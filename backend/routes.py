from flask import Blueprint, jsonify, request
import cv2
from os import makedirs
from os.path import splitext, basename, join
from io import BytesIO
import requests
from .firebase_config import bucket, db
import os
import shutil

video_processing_blueprint = Blueprint("video_processing", __name__)

@video_processing_blueprint.route("/process_video", methods=["POST"])
def process_video():
    # フロントエンドから送信されたファイルを取得
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "ファイルがありません"}), 400

    # 動画ファイルを一時保存
    video_path = join("backend/video", file.filename)
    file.save(video_path)
    
    # Firestoreのコレクション名とドキュメントIDの設定
    collection_name = "frame"  
    doc_id = splitext(basename(video_path))[0]  # ドキュメントIDとして動画名の拡張子なし部分を使用

    # フレームを切り出し、Firestorageにアップロードし、URLをFirestoreに保存
    frame_dir = "backend/frame"
    image_urls = save_frames_and_upload(video_path, frame_dir, collection_name, doc_id)
    
    # 処理が完了した後に動画ファイルを削除
    try:
        os.remove(video_path)
        print(f"{video_path} has been deleted from local storage.")
    except Exception as e:
        print(f"Error deleting video file: {e}")

    try:
        shutil.rmtree(frame_dir)  # frameディレクトリとその中身を削除
        print(f"{frame_dir} directory has been deleted from local storage.")
    except Exception as e:
        print(f"Error deleting frame directory: {e}")

    # 成功メッセージを返す
    return jsonify({"message": "フレームが保存され、Firestorageにアップロードされました", "image_urls": image_urls})

# 動画からフレームを切り出して、Firestorageにアップロードし、URLをFirestoreに保存
def save_frames_and_upload(video_path: str, frame_dir: str, collection_name: str, doc_id: str, name="image", ext="jpg"):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return []

    # 動画の基本情報を取得
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_dir = join(frame_dir, splitext(basename(video_path))[0])
    makedirs(frame_dir, exist_ok=True)

    image_urls = []  # URLを格納するリスト
    idx = 0
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 1秒ごとにフレームを保存
        if frame_count % int(fps) == 0:
            filled_idx = str(idx).zfill(4)
            frame_filename = f"{join(frame_dir, name)}_{filled_idx}.{ext}"
            cv2.imwrite(frame_filename, frame)  # フレームを保存

            # Firestorageにアップロードし、URLを取得
            image_url = upload_image_to_storage(collection_name, frame_filename, f"{splitext(basename(video_path))[0]}_{filled_idx}.{ext}")
            image_urls.append(image_url)  # URLをリストに追加
            
            os.remove(frame_filename)
            idx += 1

        frame_count += 1

    cap.release()  # 処理終了後にファイルを解放
    print("Frames have been saved and uploaded to Firestorage.")

    # Firestoreに画像URLリストを保存
    save_urls_to_firestore(collection_name, doc_id, image_urls)
    return image_urls

# Firestorageに画像をアップロードして公開URLを取得
def upload_image_to_storage(collection_name: str, image_path: str, image_name: str):
    blob = bucket.blob(f"{collection_name}/{image_name}")
    blob.upload_from_filename(image_path)
    blob.make_public()  # ファイルを公開
    print('File uploaded successfully')
    return blob.public_url

# Firestoreに画像URLリストを保存
def save_urls_to_firestore(collection_name: str, doc_id: str, image_urls: list):
    markers_ref = db.collection(collection_name).document(doc_id)
    markers_ref.set({"images": image_urls})
    print("Image URLs saved to Firestore.")

# Firestoreから画像URLリストを取得するエンドポイント
@video_processing_blueprint.route("/get_image_urls/<doc_id>", methods=["GET"])
def get_image_urls(doc_id):
    collection_name = "frame"  # 使用するFirestoreコレクション名
    data = get_marker_from_firestore(collection_name, doc_id)
    
    if data and "images" in data:
        return jsonify({"image_urls": data["images"]})
    else:
        return jsonify({"image_urls": []}), 404

# Firestoreから画像URLリストを取得
def get_marker_from_firestore(collection_name: str, doc_id: str):
    doc_ref = db.collection(collection_name).document(doc_id)
    doc = doc_ref.get()
    if doc.exists:
        print(f"Document data: {doc.to_dict()}")
        return doc.to_dict()  # ドキュメントの情報を辞書形式で返す
    else:
        print("No such document!")
        return None

# URLから画像データを取得
def fetch_image_from_url(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        print(f"Failed to fetch image from {url}")
        return None
