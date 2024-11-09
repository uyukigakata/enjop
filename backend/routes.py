from flask import Blueprint, jsonify, request
import cv2
from os import makedirs
from os.path import splitext, basename, join
from io import BytesIO
import requests
from .firebase_config import bucket, db
import os
import shutil
from google.cloud import firestore, vision
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

video_processing_blueprint = Blueprint("video_processing", __name__)

# Firestore and Vision API clients
firestore_client = firestore.Client()
vision_client = vision.ImageAnnotatorClient()

@video_processing_blueprint.route("/process_video", methods=["POST"])
def process_video():
    # Retrieve the file from the request
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "ファイルがありません"}), 400

    # Temporarily save the video
    video_path = join("backend/video", file.filename)
    file.save(video_path)

    # Define Firestore collection and document ID
    collection_name = "frame"  
    doc_id = splitext(basename(video_path))[0]

    # Extract frames, upload to Firestorage, and save URLs to Firestore
    frame_dir = "backend/frame"
    image_urls = save_frames_and_upload(video_path, frame_dir, collection_name, doc_id)

    # Run the analysis on the uploaded frames
    analysis_results = analyze_images_in_frame_folder()

    # Delete the video and frame directory
    try:
        os.remove(video_path)
        shutil.rmtree(frame_dir)
    except Exception as e:
        print(f"Error deleting files: {e}")

    # Return success message and analysis results
    return jsonify({
        "message": "フレームが保存され、Firestorageにアップロードされました",
        "image_urls": image_urls,
        "analysis_results": analysis_results
    })

# Video to frame extraction and upload function (same as before)
def save_frames_and_upload(video_path, frame_dir, collection_name, doc_id, name="image", ext="jpg"):
    # Existing frame extraction code here...
    # After uploading frames, return image_urls
    return image_urls

# Firestore and Vision API-based analysis function
def analyze_images_in_frame_folder():
    bucket_name = os.getenv("STORAGEBUCKET")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix="frame/")

    results = []
    for blob in blobs:
        if blob.name.endswith(".jpg"):
            image_uri = f"gs://{bucket_name}/{blob.name}"
            print(f"Analyzing: {image_uri}")

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
    
    # Save analysis results to Firestore
    save_analysis_results(results)
    return results

def save_analysis_results(results):
    collection_ref = firestore_client.collection("image_analysis_results")
    for result in results:
        collection_ref.add(result)
    print("Analysis results saved to Firestore.")
