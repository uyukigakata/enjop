import firebase_admin
from firebase_admin import credentials, firestore, storage
#from .config import FIREBASE_CREDENTIALS_PATH
import os
from backend.config import FIREBASE_CREDENTIALS_PATH, STORAGE_BUCKET


# Firebaseの初期化
if not firebase_admin._apps:  # 既に初期化されているかどうかを確認
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred, {
        "storageBucket": STORAGE_BUCKET
    })

# Firebaseアプリの初期化
db = firestore.client()
bucket = storage.bucket()