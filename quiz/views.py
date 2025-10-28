from django.views.generic import TemplateView, ListView
from .models import Question, Result
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.db.models import Case, When

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import QuestionSerializer


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
    

