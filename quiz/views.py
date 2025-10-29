from django.views.generic import TemplateView, ListView
from .models import Question, Result
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.db.models import Case, When

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import QuestionSerializer, ResultSerializer


class IndexView(TemplateView):
    """
    トップページを表示するクラスベースビュー
    """
    # 表示するテンプレート（HTML）ファイルを指定する
    template_name = 'quiz/index.html'


class QuizAPIView(APIView):
    """
    ランダムなクイズ10問をJSONで返すAPIビュー
    """
    # 認証: ログインしているユーザーのみアクセス許可
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        GETリクエスト（クイズ取得）に応答する
        """
        # ランダムに10件取得
        questions = Question.objects.order_by('?')[:10]

        # 1. で作成したシリアライザを使ってJSONに変換 (many=True で複数件対応)
        serializer = QuestionSerializer(questions, many=True)

        # JSONデータをレスポンスとして返す
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        POSTリクエスト（解答送信）に応答する
        (これは3日目以降に実装します)
        """
        # (今はまだ実装しないので、ダミーのレスポンスを返す)
        return Response({"message": "採点APIはまだ実装されていません"}, status=400)
    

class QuizSubmitAPIView(APIView):
    """
    クイズの解答を受け取り、採点してResultを保存するAPIビュー
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        # Vueから送られてくる解答データの想定:
        # request.data = [
        #   {"question_id": 5, "selected_answer": "A"},
        #   {"question_id": 12, "selected_answer": "C"}, ...
        # ]
        answers_data = request.data 

        if not isinstance(answers_data, list):
            return Response({"error": "不正なデータ形式です。"}, status=400)

        result_ids = []
        question_ids = [ans['question_id'] for ans in answers_data if 'question_id' in ans]

        # 関連する Question を一括で取得 (効率化)
        questions = Question.objects.filter(id__in=question_ids).in_bulk()

        results_to_create_or_update = []
        for answer_data in answers_data:
            question_id = answer_data.get('question_id')
            selected_answer = answer_data.get('selected_answer')
            question = questions.get(question_id)

            if not question or not selected_answer:
                continue # 不正なデータはスキップ

            is_correct = (selected_answer == question.correct_answer)
            
            # update_or_create を直接使うのではなく、後で一括処理する準備
            results_to_create_or_update.append(
                Result(
                    user=user,
                    question=question,
                    selected_answer=selected_answer,
                    is_correct=is_correct
                )
            )

        # bulk_update または bulk_create でDBへの書き込みを効率化 (ここは少し複雑なので、単純化も可)
        # ここでは単純化のため、１件ずつ update_or_create する
        for result_obj in results_to_create_or_update:
             result, created = Result.objects.update_or_create(
                user=result_obj.user,
                question=result_obj.question,
                defaults={
                    'selected_answer': result_obj.selected_answer,
                    'is_correct': result_obj.is_correct
                }
            )
             result_ids.append(result.id)


        # 採点した Result の ID リストをセッションに保存 (これはVue側で状態管理するため不要かも)
        # request.session['latest_result_ids'] = result_ids 
        
        # 代わりに、作成された Result の ID リストを返す
        return Response({"result_ids": result_ids}, status=201) # 201 Created


class QuizResultAPIView(APIView):
    """
    指定された Result ID リストに基づいて、採点結果 (Result + Question詳細) を返すAPIビュー
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Vueから GET パラメータで result_ids を受け取る想定
        # 例: /api/results/?ids=10,15,22,...
        result_ids_str = request.query_params.get('ids', '')
        if not result_ids_str:
             return Response({"error": "結果IDが指定されていません。"}, status=400)
        
        try:
            result_ids = [int(id_str) for id_str in result_ids_str.split(',')]
        except ValueError:
             return Response({"error": "結果IDの形式が不正です。"}, status=400)
        
        user = request.user

        # セッションの順序保持ロジック (Case/When) を使う
        preserved_order = Case(
            *[When(id=id_val, then=pos) for pos, id_val in enumerate(result_ids)]
        )
        
        # ログインユーザー自身の、指定されたIDの結果のみを取得し、順序を保持
        results = Result.objects.filter(
            id__in=result_ids, 
            user=user # 他のユーザーの結果を見せないように
        ).select_related('question').order_by(preserved_order)

        # ResultSerializer を使ってJSONに変換
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)
