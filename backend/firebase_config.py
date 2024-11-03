import firebase_admin
from firebase_admin import credentials, firestore, storage
from .config import FIREBASE_CREDENTIALS_PATH
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Firebaseの初期化
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
storageBucket =os.getenv('STORAGEBUCKET')

firebase_admin.initialize_app(cred, {
    "storageBucket":storageBucket  
})

# Firebaseアプリの初期化
db = firestore.client()
bucket = storage.bucket()