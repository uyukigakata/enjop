import os
from dotenv import load_dotenv

load_dotenv()  # .envファイルを読み込み

DEBUG = True
# OpenAI APIキーの設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
