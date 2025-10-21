from django.urls import path
from . import views  # views.py をインポート

urlpatterns = [
    # views.IndexView クラスを .as_view() メソッドで呼び出す
    path('', views.IndexView.as_view(), name='index'),
]