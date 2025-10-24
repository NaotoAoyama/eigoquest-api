from django.views.generic import TemplateView, ListView
from .models import Question, Result
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy


class IndexView(TemplateView):
    """
    トップページを表示するクラスベースビュー
    """
    # 表示するテンプレート（HTML）ファイルを指定する
    template_name = 'quiz/index.html'


class QuizView(LoginRequiredMixin, ListView):
    """
    ランダムなクイズ問題を10問表示する
    """
    model = Question               # 1. どのモデルからデータを取得するか
    template_name = 'quiz/quiz.html'    # 2. どのHTMLを使って表示するか
    context_object_name = 'questions' # 3. HTML側に渡す変数名 (default: object_list)

    # ログインしていない場合の転送先 (開発中は管理画面のログインが便利)
    login_url = reverse_lazy('accounts:login')


    def get_queryset(self):
        queryset = super().get_queryset().order_by('?')[:10]

        return queryset

    
    def post(self, request, *args, **kwargs):
        user = request.user
        
        # セッションに保存する、採点結果IDのリスト
        result_ids = []

        # フォームから送られてきたデータをループ処理
        # (例: 'question_5': 'A', 'question_12': 'C', ...)
        for key, value in request.POST.items():
            if key.startswith('question_'):
                # 'question_5' から '5' (ID) を取り出す
                question_id = int(key.split('_')[1])
                selected_answer = value

                try:
                    question = Question.objects.get(id=question_id)
                    
                    # 正誤判定
                    is_correct = (selected_answer == question.correct_answer)
                    
                    # 解答履歴 (Result) をDBに保存
                    # 既に同じ問題に答えていたら更新、なければ新規作成
                    result, created = Result.objects.update_or_create(
                        user=user,
                        question=question,
                        defaults={
                            'selected_answer': selected_answer,
                            'is_correct': is_correct
                        }
                    )
                    result_ids.append(result.id)

                except Question.DoesNotExist:
                    # (万が一問題IDが存在しなかった場合の処理)
                    continue
        
        # 採点した結果のIDリストをセッションに保存
        request.session['latest_result_ids'] = result_ids

        # 結果表示ページ (これから作成) にリダイレクト
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
        # セッションから採点した Result の ID リストを取得
        result_ids = self.request.session.get('latest_result_ids', [])
        
        # ID リストに該当する Result のみを取得
        # 関連する Question も事前に取得 (select_related) してDB負荷を下げる
        queryset = Result.objects.filter(id__in=result_ids).select_related('question')
        
        # (セッションからデータを削除しても良いが、リロード対応のため残す)
        # if 'latest_result_ids' in self.request.session:
        #     del self.request.session['latest_result_ids']
            
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