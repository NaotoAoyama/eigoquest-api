from django.urls import path
from django.contrib.auth import views as auth_views # Django標準の認証View
from . import views # accounts/views.py をインポート

app_name = 'accounts'

urlpatterns = [
    # 1. サインアップ (これから views.py に作成)
    path('signup/', views.SignUpView.as_view(), name='signup'),

    # 2. ログイン (Django標準の LoginView を使用)
    path('login/', 
         auth_views.LoginView.as_view(template_name='accounts/login.html'), 
         name='login'),

    # 3. ログアウト (Django標準の LogoutView を使用)
    path('logout/', 
         auth_views.LogoutView.as_view(), 
         name='logout'),

     # 新規登録API (POST)
    path('api/signup/', views.SignUpAPIView.as_view(), name='signup_api'),
]