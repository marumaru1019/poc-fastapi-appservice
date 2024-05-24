# ベースイメージとしてPythonを使用
FROM python:3.11

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコンテナにコピー
COPY . /app

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# ポートを公開
EXPOSE 8000

# FastAPIアプリケーションを起動するコマンド
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]