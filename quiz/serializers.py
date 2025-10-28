from rest_framework import serializers
from .models import Question

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