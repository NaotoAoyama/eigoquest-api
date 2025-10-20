# quiz/admin.py
from django.contrib import admin
from .models import Question  # 1. Question モデルをインポート

# 2. (推奨) 管理画面での表示をカスタマイズするクラスを作成
class QuestionAdmin(admin.ModelAdmin):
    # 一覧画面に表示するフィールド
    list_display = ('id', 'part', 'question_text_short', 'difficulty_level', 'created_at')
    # 絞り込み（フィルター）に使うフィールド
    list_filter = ('part', 'difficulty_level')
    # 検索ボックスで検索対象にするフィールド
    search_fields = ('question_text', 'explanation')

    # question_textが長すぎるので、一覧用に短い版を定義
    def question_text_short(self, obj):
        return obj.question_text[:40] + '...' if len(obj.question_text) > 40 else obj.question_text
    question_text_short.short_description = "問題文" # 列のタイトル

# 3. 管理画面に Question モデルを登録 (カスタマイズした QuestionAdmin も一緒に)
admin.site.register(Question, QuestionAdmin)