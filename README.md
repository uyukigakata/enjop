# SecHack365_4C_enjo

### Google cloud (vision APIの環境設定)
>pip install google-cloud-vision

### visionAPIの環境変数

.envファイル作成
>GOOGLE_APPLICATION_CREDENTIALS ="path\to\your-service-account-file.json"


### 仮想環境
>python -m venv venv

### パッケージインストール

>pip install google-cloud-vision 
>pip install google-cloud-speech
>pip install python-dotenv 
>pip install opencv-python

### 仮想環境を取り込む

venvの中身を生成（確認）
>pip freeze > requirements.txt

他の環境で同じ依存データをインストールする方法
>pip install -r requirements.txt
