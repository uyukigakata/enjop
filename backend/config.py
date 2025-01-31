import os
from dotenv import load_dotenv

load_dotenv()  #.envファイルをロード

DEBUG = True

# OpenAI APIキーの設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
