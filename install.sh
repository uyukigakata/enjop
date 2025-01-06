#!/bin/bash

# 必要なパッケージをインストール
apt update
apt install -y ffmpeg python3-pip git　python3-devel

# 作業ディレクトリに移動
# cd $HOME

# リポジトリをクローン
# git clone https://github.com/uyukigakata/SecHack365_4C_enjo.git
# cd SecHack365_4C_enjo

# 仮想環境の作成
python3 -m venv .venv
source .venv/bin/activate

# 必要なパッケージをインストール
pip install Cython
pip install wheel
git clone https://github.com/reazon-research/ReazonSpeech
pip install -r requirements.txt

# APIキーを入力として受け取る
read -p "OpenAIのAPIキーを入力してください Please Type here openai apikey" API_KEY

# .envファイルにAPIキーを書き込む
echo "OPENAI_API_KEY="$API_KEY"" > .env

<< COMMENTOUT
# デモーん化するためにsystemdサービスファイルを作成
echo "
[Unit]
Description=Gunicorn instance to serve Flask App
After=network.target
[Service]
User=sechack
Group=www-data
WorkingDirectory=/home/sechack/SecHack365_4C_enjo
ExecStart=/home/sechack/SecHack365_4C_enjo/.venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 server:app
Restart=always
Environment=PATH=/home/sechack/SecHack365_4C_enjo/.venv/bin
[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/sechack_service.service
# サービスを有効化して起動
systemctl daemon-reload
systemctl enable sechack_service.service
systemctl start sechack_service.service
COMMENTOUT

echo "サービスのインストールと起動が完了しました。APIキーは.envに保存されました。"
