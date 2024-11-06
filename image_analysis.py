from dotenv import load_dotenv
import os
from google.cloud import vision

# .envファイルの内容を読み込む
load_dotenv()

# Vision APIクライアントの初期化
client = vision.ImageAnnotatorClient()

# 画像ファイルを読み込み
with open("C:/Users/yuu/Document/prpduct/SeckHack/SecHack365_4C_enjo/model/oden.png", "rb") as image_file:
    content = image_file.read()
image = vision.Image(content=content)

# 安全検索のリクエストを送信
response = client.safe_search_detection(image=image)
safe = response.safe_search_annotation

# 評価説明を生成する関数
def explain_rating(label, score):
    explanations = {
        "VERY_UNLIKELY": "問題のあるコンテンツが含まれる可能性は極めて低いです。",
        "UNLIKELY": "問題のあるコンテンツが含まれる可能性は低いです。",
        "POSSIBLE": "問題のあるコンテンツが含まれる可能性があります。",
        "LIKELY": "問題のあるコンテンツが含まれる可能性が高いです。",
        "VERY_LIKELY": "問題のあるコンテンツが含まれる可能性が非常に高いです。",
    }
    return f"{label}: {explanations.get(score, '評価不明')}"

# 各評価の説明文を生成
print("成人向けコンテンツ(adult):", explain_rating("成人向けコンテンツ", safe.adult))
print("暴力的なコンテンツ(violence):", explain_rating("暴力的なコンテンツ", safe.violence))
print("不快なコンテンツ(Racy):", explain_rating("不快なコンテンツ", safe.racy))
print("ドラッグ関連コンテンツ(Spoof):", explain_rating("ドラッグ関連コンテンツ", safe.spoof))
