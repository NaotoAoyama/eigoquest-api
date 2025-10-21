from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    """
    TOEICの問題（主にPart 5）を格納するモデル
    """

    # 選択肢の定義
    PART_CHOICES = (
        ('PART5', 'Part 5'),
        ('PART7', 'Part 7'),
        # 必要に応じて他のパートも追加
    )

    ANSWER_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )

    # 問題文 (長文の可能性も考慮し TextField)
    question_text = models.TextField(verbose_name="問題文")

    # 選択肢
    option_a = models.CharField(max_length=255, verbose_name="選択肢 A")
    option_b = models.CharField(max_length=255, verbose_name="選択肢 B")
    option_c = models.CharField(max_length=255, verbose_name="選択肢 C")
    option_d = models.CharField(max_length=255, verbose_name="選択肢 D")

    # 解答と解説
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES, verbose_name="正解")
    explanation = models.TextField(verbose_name="解説", blank=True, null=True) # 解説は任意

    # 問題の属性
    part = models.CharField(max_length=5, choices=PART_CHOICES, default='PART5', verbose_name="パート")
    difficulty_level = models.IntegerField(default=600, verbose_name="難易度レベル (目安スコア)")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    def __str__(self):
        # 管理画面などで見やすくするための設定
        return f"{self.part} (ID: {self.id}) - {self.question_text[:20]}..."

    class Meta:
        # 管理画面での表示名を指定
        verbose_name = "問題"
        verbose_name_plural = "問題一覧"


class Result(models.Model):
    """
    ユーザーの解答履歴を保存するモデル
    """
    
    # 1. ユーザーとの連携 (ForeignKey)
    # どのユーザーが答えたか？
    # Userモデルが削除されたら、この解答履歴も一緒に削除する (CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="解答者")
    
    # 2. 問題との連携 (ForeignKey)
    # どの問題に答えたか？
    # Questionモデルが削除されたら、この解答履歴も一緒に削除する (CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="対象問題")
    
    # 3. ユーザーの選択
    selected_answer = models.CharField(max_length=1, choices=Question.ANSWER_CHOICES, verbose_name="ユーザーの選択")
    
    # 4. 正誤判定
    is_correct = models.BooleanField(default=False, verbose_name="正解フラグ")
    
    answered_at = models.DateTimeField(auto_now_add=True, verbose_name="解答日時")

    def __str__(self):
        return f"{self.user.username} -> {self.question.id} (正解: {self.is_correct})"

    class Meta:
        verbose_name = "解答履歴"
        verbose_name_plural = "解答履歴一覧"
        
        # (推奨) 1ユーザーが1問題に1回だけ答えられるように制約
        constraints = [
            models.UniqueConstraint(fields=['user', 'question'], name='unique_user_question')
        ]