from django.urls import path
from . import views  

app_name = 'quiz'

urlpatterns = [
    # views.IndexView クラスを .as_view() メソッドで呼び出す
    path('', views.IndexView.as_view(), name='index'),

    # 変更前: path('quiz/', views.QuizView.as_view(), name='quiz_page'),
    # 変更後:
    path('api/quiz/', views.QuizAPIView.as_view(), name='quiz_api'),
]