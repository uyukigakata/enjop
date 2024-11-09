import os
from dotenv import load_dotenv

load_dotenv()  # .envファイルを読み込み

DEBUG = True
# Firebaseのサービスアカウントキーのパスは .env ファイルから取得
FIREBASE_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_FIREBASE")
STORAGE_BUCKET = os.getenv("STORAGEBUCKET")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')