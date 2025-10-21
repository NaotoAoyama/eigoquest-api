EigoQuest (仮) - Django製 TOEIC学習アプリケーション
1. プロジェクト概要
EigoQuest は、TOEIC Part 5（短文穴埋め問題）形式のクイズに挑戦できるWebアプリケーションです。 このプロジェクトは、Djangoフレームワークを使用したバックエンド開発スキルを証明するためのポートフォリオとして構築しました。

単なるCRUD（作成・読込・更新・削除）機能に留まらず、データベース設計、ユーザー認証、セッション管理、クラスベースビュー（CBV）の活用など、実務的なWebアプリケーション開発に必要な要素を網羅することを目的としています。

本番デプロイ先URL: [デプロイが完了したら、ここにURLを記載]

制作期間: 2025年10月20日〜

2. 主な機能
ランダムクイズ機能: データベースに登録された問題から、ランダムに10問を抽出して出題します。

自動採点機能: ユーザーが送信した解答をサーバーサイドで自動採点し、正解・不正解を判定します。

結果表示と解説: 採点結果（正解数）と共に、各問題の正解と詳細な解説を表示します。

解答履歴の保存: Result モデルにより、どのユーザー（User）がどの問題（Question）にどう解答したかを記録します。

問題管理機能 (Django Admin): Djangoの管理画面から、TOEIC問題の追加・編集・削除が可能です。

3. 使用技術
こだわった点や、ポートフォリオとしてアピールしたい技術スタックを記載します。

バックエンド
Python (3.12.3)

Django (5.2.7)

クラスベースビュー (CBV): TemplateView, ListView を継承し、ロジックをクラスとして整理。

Django ORM: ForeignKey を用いた User, Question, Result のリレーショナルデータベース設計。

認証・セッション: LoginRequiredMixin によるアクセスコントロールと、セッション（request.session）を用いた採点結果の受け渡し。

Django Admin: モデルの管理画面をカスタマイズ（list_display, list_filter 等）。

データベース
PostgreSQL: 本番環境を想定した堅牢なRDBMSを採用。

フロントエンド
HTML / CSS: Djangoテンプレートシステム（DTL）による動的なページ生成。
JavaScriptの導入は未定。今後の進捗により検討する。

インフラ・その他
環境: Ubuntu, VSCode

仮想環境: Python venv

バージョン管理: Git / GitHub

セキュリティ: python-decouple を使用し、.env ファイルによる秘密鍵・パスワードの安全な管理。

デプロイ (予定): [Render, Heroku, AWSなど、予定している環境]

4. 開発環境のセットアップ (ローカル)
このリポジトリをローカルで実行する手順です。

Bash

# 1. リポジトリをクローン
git clone https://github.com/[Your Name]/eigoquest.git
cd eigoquest

# 2. 仮想環境の作成とアクティベート
python3 -m venv venv
source venv/bin/activate

# 3. 必要なライブラリのインストール
pip install -r requirements.txt

# 4. PostgreSQLでデータベースとユーザーを作成
# (手順は割愛。eigoquest_db, eigoquest_user を作成想定)

# 5. .env ファイルの作成
# .gitignore されている .env ファイルをルートに作成し、DB情報やSECRET_KEYを記述
# (例)
# SECRET_KEY=your_django_secret_key
# DEBUG=True
# DB_NAME=eigoquest_db
# DB_USER=eigoquest_user
# DB_PASSWORD=your_db_password
# DB_HOST=localhost

# 6. データベースのマイグレーション
python3 manage.py migrate

# 7. 管理者アカウントの作成
python3 manage.py createsuperuser

# 8. 開発サーバーの起動
python3 manage.py runserver
管理画面 (http://127.0.0.1:8000/admin/) にログイン後、問題を登録するとクイズ機能 (http://127.0.0.1:8000/quiz/) がテスト可能です。