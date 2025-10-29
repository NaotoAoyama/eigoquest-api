"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # トップページ ('') へのアクセスが来たら、
    # quizアプリ内の urls.py を見に行くよう設定
    path('', include('quiz.urls')),
    path('accounts/', include('accounts.urls')),
    # JWT トークン取得 (ログイン) API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # JWT トークンリフレッシュ API
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
