from django.views.generic import TemplateView, ListView
from .models import Question


class IndexView(TemplateView):
    """
    トップページを表示するクラスベースビュー
    """
    # 表示するテンプレート（HTML）ファイルを指定する
    template_name = 'quiz/index.html'


class QuizView(ListView):
    """
    ランダムなクイズ問題を10問表示する
    """
    model = Question               # 1. どのモデルからデータを取得するか
    template_name = 'quiz/quiz.html'    # 2. どのHTMLを使って表示するか
    context_object_name = 'questions' # 3. HTML側に渡す変数名 (default: object_list)

    def get_queryset(self):
        """
        クエリセットをカスタマイズして、ランダムな10件を取得する
        """
        # Question.objects.order_by('?') でランダムに並び替え、
        # [:10] で最初の10件を取得する
        queryset = super().get_queryset().order_by('?')[:10]
        return queryset