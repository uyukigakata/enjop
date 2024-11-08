import firebase_admin
from firebase_admin import credentials, firestore, storage
#from .config import FIREBASE_CREDENTIALS_PATH
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))


# Firebaseの初期化
cred_path = os.getenv("GOOGLE_APPLICATION_FIREBASE")

if not cred_path or not os.path.exists(cred_path):
    raise FileNotFoundError(f"Firebase認証ファイルが見つからない")

cred = credentials.Certificate(cred_path)

firebase_admin.initialize_app(cred, {
    "storageBucket": os.getenv("STORAGEBUCKET")
})

# Firebaseアプリの初期化
db = firestore.client()
bucket = storage.bucket()