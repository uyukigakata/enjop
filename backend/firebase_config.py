import firebase_admin
from firebase_admin import credentials, firestore, storage
#from .config import FIREBASE_CREDENTIALS_PATH
import os
from backend.config import FIREBASE_CREDENTIALS_PATH, STORAGE_BUCKET


# Firebaseの初期化
if not FIREBASE_CREDENTIALS_PATH or not os.path.exists(FIREBASE_CREDENTIALS_PATH):
    raise FileNotFoundError(f"Firebase認証ファイルが見つからない")

cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)

firebase_admin.initialize_app(cred, {
    "storageBucket": STORAGE_BUCKET
})

# Firebaseアプリの初期化
db = firestore.client()
bucket = storage.bucket()