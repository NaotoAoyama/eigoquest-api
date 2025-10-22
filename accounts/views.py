# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUpView(generic.CreateView):
    """
    サインアップ（新規ユーザー登録）ビュー
    """
    form_class = UserCreationForm
    # 登録が成功した後のリダイレクト先 (ログインページ)
    success_url = reverse_lazy('accounts:login') 
    # 表示するテンプレート
    template_name = 'accounts/signup.html'