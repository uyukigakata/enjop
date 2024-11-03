from flask import Flask
from flask_cors import CORS
import os
from backend.firebase_config import db  # 絶対パスでインポート
from .views import video_processing_blueprint  # 相対インポートに変更


def create_app():
    app = Flask(__name__)
    CORS(app)  # CORSを有効化

    # config.py を直接パスで指定
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), 'config.py'))
    
    # Blueprintの登録
    app.register_blueprint(video_processing_blueprint, url_prefix="/api")


    # シンプルなテストルートを定義
    @app.route('/')
    def index():
        return 'Hello World!'

    @app.route('/test')
    def other1():
        return "テストページです！"

    return app
