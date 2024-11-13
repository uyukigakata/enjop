# SecHack365_4C_enjo

## APIの設定

### Google cloud API visionAPI、speech-to-textの環境変数作成
```bash
GOOGLE_APPLICATION_CREDENTIALS ="path\to\your-service-account-file.json"
```

### Open APIの環境変数作成
```bash
OPENAI_API_KEY = "APIキー"
```

### 仮想環境作成方法

```bash
python -m venv venv
```

### パッケージインストール
```bash
pip install google-cloud-vision 
pip install google-cloud-speech
pip install python-dotenv 
pip install openai
```

### 仮想環境を取り込む

venvの中身を生成（確認）
```bash
pip freeze > requirements.txt
```

他の環境で同じ依存データをインストールする方法
```bash
pip install -r requirements.txt
```

# SecHack365_4C_enjo

