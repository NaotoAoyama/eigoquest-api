from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import SignUpSerializer
from django.contrib.auth.models import User


class SignUpView(generic.CreateView):
    """
    サインアップ（新規ユーザー登録）ビュー
    """
    form_class = UserCreationForm
    # 登録が成功した後のリダイレクト先 (ログインページ)
    success_url = reverse_lazy('accounts:login') 
    # 表示するテンプレート
    template_name = 'accounts/signup.html'


class SignUpAPIView(generics.CreateAPIView):
    """
    新規ユーザー登録（サインアップ）のためのAPIビュー
    """
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    # 認証: 誰でも (AllowAny) アクセスできるように設定
    permission_classes = [permissions.AllowAny]