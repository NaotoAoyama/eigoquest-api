from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password # (任意) パスワード強度チェック
from rest_framework.validators import UniqueValidator

class SignUpSerializer(serializers.ModelSerializer):
    """
    新規ユーザー登録（サインアップ）用シリアライザ
    """
    # ユーザー名の重複チェックを（デフォルトより親切なエラーメッセージで）追加
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="このユーザー名は既に使用されています。")]
    )
    # パスワードは書き込み専用（APIで読み取れないように）
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password] # Django標準のパスワード強度チェック
    )
    # パスワード（確認用）
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm') # APIが受け取るフィールド

    def validate(self, attrs):
        """
        パスワードとパスワード（確認用）が一致するかチェック
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "パスワードが一致しません。"})
        return attrs

    def create(self, validated_data):
        """
        バリデーション通過後にユーザーを作成する (パスワードをハッシュ化する)
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            # validated_data['password'] をそのまま使わず、create_user でハッシュ化
        )
        user.set_password(validated_data['password'])
        user.save()

        return user