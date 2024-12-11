# ベースイメージとしてUbuntuを使用
FROM ubuntu:20.04

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-opencv \
    curl \
    ffmpeg\
    && apt-get clean

# Ollamaのインストール
RUN curl -fsSL https://ollama.com/install.sh | sh

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY requirements.txt requirements.txt
COPY . .

# Pythonパッケージをインストール
RUN pip3 install --no-cache-dir -r requirements.txt\
&& git clone https://github.com/reazon-research/ReazonSpeech
&& pip install Cython
&& pip install ReazonSpeech/pkg/nemo-asr


# FlaskアプリケーションとOllamaを実行
CMD ["sh", "-c", "ollama run llava & python3 sever.py"]