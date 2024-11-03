import firebase_admin
from firebase_admin import credentials, firestore
from .config import FIREBASE_CREDENTIALS_PATH

# Firebaseの初期化
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)

# Firestoreのデータベースにアクセス
db = firestore.client()
