from flask import Flask,render_template,send_from_directory
from flask_cors import CORS
import os
from backend.routes import video_processing_blueprint  # 相対インポートに変更
from backend.routes import bluesky_blueprint
def create_app():
    app = Flask(__name__)
    CORS(app)  # CORSを有効化

    # config.py を直接パスで指定
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), 'config.py'))
    
    # Blueprintの登録
    app.register_blueprint(video_processing_blueprint, url_prefix="/api")
    app.register_blueprint(bluesky_blueprint,url_prefix="/api")

    # シンプルなテストルートを定義
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def index(path):
        return render_template("index.html")
    
    # assets ディレクトリのファイルを返すルートを定義
    @app.route('/assets/<path:path>')
    def send_assets(path):
        return send_from_directory(os.path.join(app.root_path, 'templates/assets'), path)

    return app