# backend/analyze_gcs_images.py
from google.cloud import storage, vision, firestore
from dotenv import load_dotenv
import os

# .env ファイルの内容を読み込む
load_dotenv()

# 認証情報を設定してGoogle Cloudクライアントを初期化
storage_client = storage.Client.from_service_account_json(os.getenv("GOOGLE_APPLICATION_FIREBASE"))
vision_client = vision.ImageAnnotatorClient.from_service_account_json(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
firestore_client = firestore.Client.from_service_account_json(os.getenv("GOOGLE_APPLICATION_FIREBASE"))

bucket_name = os.getenv("STORAGEBUCKET")
bucket = storage_client.bucket(bucket_name)

# GCS 内の frame フォルダの画像を分析
def analyze_images_in_frame_folder():
    blobs = bucket.list_blobs(prefix="frame/")

    results = []
    for blob in blobs:
        if blob.name.endswith(".jpg"):
            # 画像 URI を取得
            image_uri = f"gs://{bucket_name}/{blob.name}"
            print(f"Analyzing: {image_uri}")
            
            # Vision API で安全検索を実行
            image = vision.Image()
            image.source.image_uri = image_uri
            response = vision_client.safe_search_detection(image=image)
            safe = response.safe_search_annotation

            result = {
                "image": image_uri,
                "adult": safe.adult,
                "violence": safe.violence,
                "racy": safe.racy
            }
            results.append(result)
    
    # Firestore に保存
    save_analysis_results(results)

# Firestore に分析結果を保存する
def save_analysis_results(results):
    collection_ref = firestore_client.collection("image_analysis_results")
    for result in results:
        collection_ref.add(result)
    print("Analysis results saved to Firestore.")

# 実行
if __name__ == "__main__":
    analyze_images_in_frame_folder()
