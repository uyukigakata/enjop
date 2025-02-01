from flask import Blueprint, jsonify, request
import cv2
import os
from os import makedirs
from os.path import splitext, basename, join
from io import BytesIO
import requests
import openai
import shutil
import base64
import json
import numpy as np
from ollama import chat
from ollama import ChatResponse
from reazonspeech.nemo.asr import load_model, transcribe, audio_from_path
from dotenv import load_dotenv
import uuid
import subprocess

load_dotenv()
# Blueprintの初期化(video・bluesky)
video_processing_blueprint = Blueprint("video_processing", __name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# OpenAI APIキーの設定
openai.api_key = os.getenv("OPENAI_API_KEY")
# Pytouchの推論デバイスをCPUに指定
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
model = load_model(device='cpu')

"""
------------------------------------------------------------------
以下、video_processing_blueprint(動画をLLMに投げるまわり)のエンドポイント
------------------------------------------------------------------
"""

# URLから画像データを取得する関数
def fetch_image_from_url(url: str):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            print(f"URLから画像を取得できませんでした: {url}")
            return None
    except Exception as e:
        print(f"画像取得エラー ({url}): {e}")
        return None

# 動画の音声を文字起こしする関数
def transcribe_audio(video_path):
    try:
        # ffmpegで音声トラックが存在するか確認
        check_audio_command = f"ffmpeg -i {video_path} -map 0:a -c copy -f null -"
        result = subprocess.run(check_audio_command, shell=True, stderr=subprocess.PIPE)

        # エラー出力に "Stream map '0:a' matches no streams." が含まれていたら音声なし
        if b"matches no streams" in result.stderr:
            print("音声トラックが見つかりませんでした")
            return "音声トラックがありません"

        # 音声抽出コマンド
        audio_path = join(basedir, "audio.wav")
        extract_audio_command = f"ffmpeg -i {video_path} -ar 16000 -map a {audio_path}"
        os.system(extract_audio_command)

        # 文字起こし
        audio = audio_from_path(audio_path)
        transcription = transcribe(model, audio)
        transcription_text = transcription.text
        print(transcription_text)

        # 音声ファイルを削除
        os.remove(audio_path)
        return transcription_text
    except Exception as e:
        print(f"音声文字起こしエラー: {e}")
        return "音声文字起こし中にエラーが発生しました"


# フロントから動画ファイルを受け取り、処理を行うエンドポイント
@video_processing_blueprint.route("/process_video", methods=["POST"])
def process_video():
    try:
        content_str = request.form.get("content_str", "")
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "ファイルがありません"}), 400

        # ファイル名をUTFで英語に
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        video_dir = join(basedir, "video")
        os.makedirs(video_dir, exist_ok=True)
        video_path = join(video_dir, unique_filename)
        file.save(video_path)
        print(f"動画ファイルを保存しました: {video_path}")

        # フレームを保存
        frame_dir = join(basedir, "frame")
        os.makedirs(frame_dir, exist_ok=True)
        image_paths = save_frames(video_path, frame_dir)

        # 音声を文字起こし
        transcription_text = transcribe_audio(video_path)

        # analyze_imagesにimageをわたす。
        analysis_response = requests.post(
            "http://localhost:5000/api/analyze_images",
            json={
                "content_str": content_str,
                "image_paths": image_paths,  # image_paths をリストとして渡す
                "transcription": transcription_text
            }
        )

        # 不要なファイルとフォルダを削除
        os.remove(video_path)
        shutil.rmtree(frame_dir)

        if analysis_response.status_code == 200:
            return jsonify(analysis_response.json()), 200
        else:
            return jsonify({"error": "画像分析中にエラーが発生しました"}), 500

    except Exception as e:
        print(f"動画処理中にエラーが発生しました: {e}")
        return jsonify({"error": "動画の処理中にエラーが発生しました"}), 500

# フロントから動画ファイルを受け取り、処理を行うエンドポイント
@video_processing_blueprint.route("/process_image", methods=["POST"])
def process_image():
    try:
        content_str = request.form.get("content_str", "")
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "ファイルがありません"}), 400

        #ファイル名をUTFで英語に
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        image_dir = join(basedir, "image")
        os.makedirs(image_dir, exist_ok=True)
        image_path = join(image_dir, unique_filename)
        file.save(image_path)
        print(f"画像ファイルを保存しました: {image_path}")

        #　analyze_imagesにimageをわたす。
        analysis_response = requests.post(
            "http://localhost:5000/api/analyze_images",
                json={
                    "content_str": content_str,
                    "image_paths": [image_path],         # image_paths を追加
    }
        )

        # 不要なファイルとフォルダを削除
        os.remove(image_path)

        if analysis_response.status_code == 200:
            return jsonify(analysis_response.json()), 200
        else:
            return jsonify({"error": "画像分析中にエラーが発生しました"}), 500

    except Exception as e:
        print(f"画像処理中にエラーが発生しました: {e}")
        return jsonify({"error": "画像の処理中にエラーcが発生しました"}), 500

def process_text():
    try:
        content_str = request.form.get("content_str", "")
        if not content_str:
            return jsonify({"error": "テキストが提供されていません"}), 400

        # テキスト分析エンドポイントに変更
        analysis_response = requests.post(
            "http://localhost:5000/api/analyze_images",
            json={
                "content_str": content_str,
                "image_paths": [],  # 空のリストを渡す
                "transcription": ""  # 空の文字列を渡す
            }
        )

        if analysis_response.status_code == 200:
            return jsonify(analysis_response.json()), 200
        else:
            return jsonify({"error": "テキスト分析中にエラーが発生しました"}), 500

    except Exception as e:
        print(f"テキスト処理中にエラーが発生しました: {e}")
        return jsonify({"error": "テキストの処理中にエラーが発生しました"}), 500
        
# max800x800のサイズにリサイズandJPEG形式で圧縮する関数
def compress_image(image_data, max_size=(600, 600), quality=85):
    # バイト列から画像を読み込み
    if isinstance(image_data, bytes):
        arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    else:
        img = cv2.imread(image_data)

    # アスペクト比を保持しながらリサイズ
    h, w = img.shape[:2]
    if w > max_size[0] or h > max_size[1]:
        ratio = min(max_size[0]/w, max_size[1]/h)
        new_size = (int(w * ratio), int(h * ratio))
        img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)

    # JPEG形式で圧縮
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, compressed = cv2.imencode('.jpg', img, encode_param)    
    return compressed.tobytes()

# 画像をBase64形式にエンコードする関数

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        compressed_image = compress_image(image_file.read())
        return base64.b64encode(compressed_image).decode('utf-8')
"""
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
"""
# ollamaのllavaを用いて、画像を説明させる関数
def analyze_image_with_ollama(image_path):
    base64_image = encode_image(image_path)

    ollama_response: ChatResponse= chat(
        model='llava', 
        messages=[
    {
        'role': 'user',
        'content': 'This video was shot in Japan. Please describe the situation on the screen as concisely as possible.',
        'images': [base64_image]
    },
    ])

    response = ollama_response.message.content
    return response
# 画像分析を行うエンドポイント(いまは、prossece_videoからのPOSTを想定)
@video_processing_blueprint.route("/analyze_images", methods=["POST"])
def analyze_images():
    try:
        transcription = request.json.get("transcription", "")
        image_paths = request.json.get("image_paths", [])
        content_str = request.json.get("content_str", "")
        
        if not image_paths:
            return jsonify({"error": "画像パスがありません"}), 400

        analysis_results = []
        for idx, image_path in enumerate(image_paths):
            if not os.path.exists(image_path):
                continue
            ollama_result = analyze_image_with_ollama(image_path)
            analysis_results.append(f"{idx+2}秒: {ollama_result}")

        if not analysis_results:
            return jsonify({"error": "有効な画像が見つかりません"}), 400

        summary_prompt = (
            f"Ollamaの結果は以下です:\n{chr(10).join(analysis_results)}\n"
            f"音声の文字起こし結果は以下です:\n{transcription}\n"
        )
        # legal_scoring.jsonの内容を読み込む
        with open('backend/legal_scoring.json', 'r', encoding='utf-8') as f:
            legal_scoring = json.load(f)

        # summary_promptにlegal_scoringの内容を追加
        summary_prompt += f"法律の情報は以下です:\n{json.dumps(legal_scoring, ensure_ascii=False)}\n"
        openai_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "投稿予定の文字列（ないかもしれない）と、動画・画像（一フレーム分の画像しかないときは画像、それ以外は動画）の分析結果・音声の文字起こしの結果について、添付された日本の法律についてのJsonファイルから、違反していそうな法律のID・法律名・今回の結果について法律の違反確率を1~10段階評価・なぜそう思ったか・その他のリスクについて、以下の様式にしたがってレスポンスを返してください。なお、レスポンスは日本語で返すこと。JSON形式で返すこと。改行文字、エスケープ文字は含まないように返してください。"},
                {"role": "system", "content": json.dumps(
                {"laws": [ 
                    { 
                        "law_id": "法律のID", 
                        "law_name": "法律名", 
                        "law_risk_level": "法律の違反確率", 
                        "law_reason": "なぜそう思ったか"
                    } 
                ],  
                "comment": "その他のリスクについて", 
                "rating": "1~10段階評価によるリスク評価"
                },ensure_ascii=False)},
                {"role": "user", "content": summary_prompt},
                {"role":"user", "content": content_str}
            ],
        )

        result = {
            "analysis_results": analysis_results,
            "openai_risk_assessment": openai_response.choices[0].message['content'].strip()
        }
        print(result)
        return jsonify(result), 200

    except Exception as e:
        print(f"画像分析中にエラーが発生しました: {e}")
        return jsonify({"error": "画像分析中にエラーが発生しました"}), 500
        
# 動画からフレームを切り出して、ローカルに保存する関数
def save_frames(video_path: str, frame_dir: str, name="image", ext="jpg"):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return []

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_dir = join(frame_dir, splitext(basename(video_path))[0])
    makedirs(frame_dir, exist_ok=True)

    image_paths = []
    idx = 0
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % int(2*fps) == 0:
            filled_idx = str(idx).zfill(4)
            frame_filename = f"{join(frame_dir, name)}_{filled_idx}.{ext}"
            cv2.imwrite(frame_filename, frame)
            image_paths.append(frame_filename)
            idx += 1

        frame_count += 1

    cap.release()
    print("Frames have been saved.")
    return image_paths  # 追加

@video_processing_blueprint.route("/upload", methods=["POST"])
def upload_file():
    try:
        file = request.files.get("file")
        content_str = request.form.get("content_str", "")
        
        if file:
            content_type = file.content_type
            print(f"Content type: {content_type}")
            # MIMEタイプに基づいて振り分け
            if content_type.startswith('image/'):
                return process_image()
            elif content_type.startswith('video/') or content_type == 'application/octet-stream':
                return process_video()
            else:
                return jsonify({"error": "未対応のファイル形式です"}), 400
        elif content_str:
            return process_text()
        else:
            return jsonify({"error": "ファイルまたはテキストが提供されていません"}), 400

    except Exception as e:
        print(f"ファイル処理中にエラーが発生しました: {e}")
        return jsonify({"error": "ファイルの処理中にエラーが発生しました"}), 500
