from dotenv import load_dotenv
import os
from google.cloud import vision

# .envファイルの内容を読み込む
load_dotenv()

# Vision APIクライアントの初期化
client = vision.ImageAnnotatorClient()

# 画像ファイルを読み込み
with open("C:/Users/yuu/Document/prpduct/SeckHack/SecHack365_4C_enjo/model/icebox.png", "rb") as image_file:
    content = image_file.read()
image = vision.Image(content=content)

# 安全検索のリクエストを送信
response = client.safe_search_detection(image=image)
safe = response.safe_search_annotation

# 結果を出力
print("成人向けコンテンツ:", safe.adult)
print("暴力的なコンテンツ:", safe.violence)
