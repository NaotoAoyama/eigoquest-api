from rest_framework import serializers
from .models import Question, Result

class QuestionSerializer(serializers.ModelSerializer):
    """
    QuestionモデルをJSONに変換するためのシリアライザ
    """
    class Meta:
        model = Question
        # JSONに含めるフィールドを指定
        fields = [
            'id', 
            'question_text', 
            'option_a', 
            'option_b', 
            'option_c', 
            'option_d',
            # 'correct_answer', # 
            # 'explanation',    # 
            # ^^^ APIでクイズを渡す時点では、正解と解説は含めない
        ]


class QuestionResultSerializer(serializers.ModelSerializer):
    """
    Questionモデルを「結果表示用」にJSON変換するシリアライザ
    (正解と解説を含む)
    """
    class Meta:
        model = Question
        # 正解と解説を含める
        fields = [
            'id', 
            'question_text', 
            'option_a', 
            'option_b', 
            'option_c', 
            'option_d',
            'correct_answer', # 正解を追加
            'explanation'     # 解説を追加
        ]

class ResultSerializer(serializers.ModelSerializer):
    """
    ResultモデルをJSONに変換するためのシリアライザ
    (関連するQuestion情報も含む)
    """
    # 関連する Question モデルの情報は QuestionResultSerializer を使う
    question = QuestionResultSerializer(read_only=True) 

    class Meta:
        model = Result
        # JSONに含めるフィールド
        fields = [
            'id', 
            'user',          # 誰が
            'question',      # どの問題に (詳細情報付き)
            'selected_answer', # どう答えたか
            'is_correct',    # 正誤
            'answered_at'    # いつ
        ]