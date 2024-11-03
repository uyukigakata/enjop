from flask import Flask
from flask_cors import CORS
import os
from backend.firebase_config import db  # 絶対パスでインポート

def create_app():
    app = Flask(__name__)
    CORS(app)  # CORSを有効化

    # config.py を直接パスで指定
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), 'config.py'))

    # シンプルなテストルートを定義
    @app.route('/')
    def index():
        return 'Hello World!'

    @app.route('/test')
    def other1():
        return "テストページです！"

    return app
