from django.views.generic import TemplateView, ListView
from .models import Question, Result
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.db.models import Case, When


class IndexView(TemplateView):
    """
    トップページを表示するクラスベースビュー
    """
    # 表示するテンプレート（HTML）ファイルを指定する
    template_name = 'quiz/index.html'


class QuizView(LoginRequiredMixin, ListView):
    model = Question
    template_name = 'quiz/quiz.html'
    context_object_name = 'questions'
    login_url = reverse_lazy('accounts:login') 

    def get_queryset(self):
        """
        クエリセットをカスタマイズして、ランダムな10件を取得する
        （DB負荷を考慮し、キャッシュは使用しない元のロジックに戻す）
        """
        queryset = super().get_queryset().order_by('?')[:10]
        return queryset

    def post(self, request, *args, **kwargs):
        """
        解答（POST）を処理する
        """
        user = request.user
        
        # 変更点: POSTデータ（request.POST）に含まれるキーを基準に処理する
        # (例: 'question_5', 'question_12', ...)
        
        result_ids = []
        question_id_map = {} # POSTされてきた順番を保持するための辞書 {id: 順序}

        # 1. POSTデータから、解答された Question の IDリスト と 順序 を抽出
        order_index = 0
        for key in request.POST.keys():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                question_id_map[question_id] = order_index
                order_index += 1
        
        question_ids = list(question_id_map.keys())

        if not question_ids:
            # 解答が一つも送られてこなかった場合
            return redirect('quiz:index') # トップに戻す

        # 2. DBからPOSTされたIDの Question をすべて取得
        questions_answered = Question.objects.filter(id__in=question_ids)

        # 3. DBから取得した Question を、POSTされた順序（=表示順）に並び替える
        preserved_order = Case(
            *[When(id=id_val, then=pos) for id_val, pos in question_id_map.items()]
        )
        questions_in_order = questions_answered.order_by(preserved_order)

        # 4. 並び替えた順序で採点し、Result ID をセッションに保存
        for question in questions_in_order:
            selected_answer = request.POST.get(f'question_{question.id}')
            
            is_correct = (selected_answer == question.correct_answer)
            
            result, created = Result.objects.update_or_create(
                user=user,
                question=question,
                defaults={
                    'selected_answer': selected_answer,
                    'is_correct': is_correct
                }
            )
            # 表示された順（POSTされた順）に Result ID をリストに追加
            result_ids.append(result.id)

        # 5. 結果ページへリダイレクト
        request.session['latest_result_ids'] = result_ids
        return redirect('quiz:result_page')

class QuizResultView(LoginRequiredMixin, ListView):
    """
    直近のクイズ結果を表示する
    """
    model = Result
    template_name = 'quiz/quiz_result.html'
    context_object_name = 'results'
    login_url = reverse_lazy('accounts:login')

    def get_queryset(self):
        result_ids = self.request.session.get('latest_result_ids', [])
        
        if not result_ids:
            return Result.objects.none() # IDがなければ空を返す

        # 変更点: セッションに保存されたIDリストの順序を保持する order_by を追加
        
        # 1. Case...When... を使って、IDリストの順序をDBの並び順として定義
        preserved_order = Case(
            *[When(id=id_val, then=pos) for pos, id_val in enumerate(result_ids)]
        )
        
        # 2. filter で絞り込み、order_by で 1. の順序を適用
        queryset = Result.objects.filter(id__in=result_ids).select_related('question').order_by(preserved_order)
            
        return queryset

    def get_context_data(self, **kwargs):
        # ListView の基本機能で context (results) を取得
        context = super().get_context_data(**kwargs)
        
        # context['results'] (queryset) はDBから取得したまま
        # 変更前（QuerySetを消費してしまう）:
        # results_list = list(context['results'])
        # correct_count = sum(1 for r in results_list if r.is_correct)
        # total_count = len(results_list)
        
        # 変更後（QuerySetを消費しない .count() を使う）:
        # context['results'] には触らず、元のQuerySet（get_queryset()）に対して集計
        results_qs = self.get_queryset()
        context['correct_count'] = results_qs.filter(is_correct=True).count()
        context['total_count'] = results_qs.count()
        
        return context