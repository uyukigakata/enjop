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
# from dotenv import load_dotenv
# import os
# from google.cloud import vision

# # .envファイルの内容を読み込む
# load_dotenv()

# # Vision APIクライアントの初期化
# client = vision.ImageAnnotatorClient()

# # 画像ファイルを読み込み
# with open("C:/Users/yuu/Document/prpduct/SeckHack/SecHack365_4C_enjo/model/sushi.png", "rb") as image_file:
#     content = image_file.read()
# image = vision.Image(content=content)

# # SafeSearchとラベル検出を行う
# response_safe = client.safe_search_detection(image=image)
# response_label = client.label_detection(image=image)
# safe = response_safe.safe_search_annotation
# labels = response_label.label_annotations

# # 炎上リスクを判断し、説明メッセージを生成する
# def analyze_content(safe, labels):
#     messages = []
    
#     # SafeSearchの成人向け・暴力的・不快な内容の評価
#     if safe.adult >= 4:
#         messages.append("成人向けの内容が含まれているため、多くの視聴者に不快感を与える可能性があります。")
#     if safe.violence >= 4:
#         messages.append("暴力的な内容が含まれているため、一部の視聴者にはショッキングに感じられる恐れがあります。")
#     if safe.racy >= 4:
#         messages.append("性的または不快に感じられる要素が含まれており、批判を受けやすくなります。")
#     if safe.spoof >= 4:
#         messages.append("いたずらや誤解を招く要素が含まれており、視聴者に不快感を与える可能性があります。")

#     # ラベル検出の内容に基づく追加判断
#     risk_labels = {"weapon", "alcohol", "nudity", "drugs"}
#     for label in labels:
#         if label.description.lower() in risk_labels:
#             messages.append(f"画像内に「{label.description}」が含まれているため、誹謗中傷や批判の対象となる可能性があります。")
    
#     if messages:
#         return "この画像は不適切と判断される可能性があります。理由:\n" + "\n".join(messages)
#     else:
#         return "この画像は特に不適切な要素は含まれていないと判断されます。"

# # 結果の出力
# print(analyze_content(safe, labels))
