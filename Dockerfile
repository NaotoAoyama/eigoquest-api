# 1. ベースイメージの指定 (Python 3.12 の軽量版)
FROM python:3.12-slim

# 2. 環境変数の設定
ENV PYTHONDONTWRITEBYTECODE 1  # .pyc ファイルを作成しない
ENV PYTHONUNBUFFERED 1         # Pythonのログをバッファせず、すぐに出力する

# 3. OS (Debian) のパッケージリストを更新し、PostgreSQLクライアントをインストール
# (psycopg2 のコンパイルに必要)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. ワーキングディレクトリの作成と設定
WORKDIR /app

# 5. requirements.txt を先にコピーし、ライブラリをインストール
# (この層をキャッシュさせるため、コード本体より先に実行)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. プロジェクトコード全体をワーキングディレクトリにコピー
COPY . .