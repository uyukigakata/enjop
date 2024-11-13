import os
from dotenv import load_dotenv

load_dotenv()  # .envファイルを読み込み

DEBUG = True
# Firebaseのサービスアカウントキーのパスは .env ファイルから取得
FIREBASE_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_FIREBASE")
#FireStoreに入れる
STORAGE_BUCKET = os.getenv("STORAGEBUCKET")
#Google Cloud APIをキー
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
# OpenAI APIキーの設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")