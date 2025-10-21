from django.urls import path
from . import views  # views.py をインポート

app_name = 'quiz'

urlpatterns = [
    # views.IndexView クラスを .as_view() メソッドで呼び出す
    path('', views.IndexView.as_view(), name='index'),

    # 'quiz/'というURLへのアクセスが来たら、views.QuizViewを呼び出す
    path('quiz/', views.QuizView.as_view(), name='quiz_page'),

    # 追記: 結果表示ページのURL
    path('result/', views.QuizResultView.as_view(), name='result_page'),
]