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
from reazonspeech.nemo.asr import load_model, transcribe, audio_from_path
from atproto import Client


# Blueprintの初期化(video・bluesky)
video_processing_blueprint = Blueprint("video_processing", __name__)
bluesky_blueprint = Blueprint("bluesky", __name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# OpenAI APIキーの設定
openai.api_key = os.getenv("OPENAI_API_KEY")
# Pytouchの推論デバイスをCPUに指定
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
model = load_model(device='cpu')

# Bluesky(atproto)のクライアントを初期化
client=Client()

# Bluesky(atproto)のクライアントをログイン(共通IDとパスワードを使用)

# Load .env file
from dotenv import load_dotenv
load_dotenv()

client.login("enjop.bsky.social", os.getenv("BLUESKY_PASSWORD"))

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
    audio_path = join(basedir, "audio.wav")
    command = f"ffmpeg -i {video_path} -ar 16000 -map a {audio_path}"  # 動画から音声を抽出して16000WAV形式に保存
    os.system(command)

    audio = audio_from_path(audio_path)
    transcription = transcribe(model, audio)
    
    # transcription オブジェクトからテキストを抽出
    transcription_text = transcription.text  # ここで transcription_text を定義
    print(transcription_text)
    
    os.remove(audio_path)
    return transcription_text

# フロントから動画ファイルを受け取り、処理を行うエンドポイント
@video_processing_blueprint.route("/process_video", methods=["POST"])
def process_video():
    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "ファイルがありません"}), 400

        video_dir = join(basedir, "video")
        os.makedirs(video_dir, exist_ok=True)
        video_path = join(video_dir, file.filename)
        file.save(video_path)
        print(f"動画ファイルを保存しました: {video_path}")

        # フレームを保存
        frame_dir = join(basedir, "frame")
        os.makedirs(frame_dir, exist_ok=True)
        image_paths = save_frames(video_path, frame_dir)

        # 音声を文字起こし
        transcription_text = transcribe_audio(video_path)

        #　analyze_imagesにimageをわたす。
        analysis_response = requests.post(
            "http://localhost:5000/api/analyze_images",
                json={
                    "image_paths": image_paths,         # image_paths を追加
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

# max800x800のサイズにリサイズandJPEG形式で圧縮する関数
def compress_image(image_data, max_size=(400, 400), quality=85):
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

# ollamaのllavaを用いて、画像を説明させる関数
def analyze_image_with_ollama(image_path):
    base64_image = encode_image(image_path)

    data = {
        'model': 'llava',
        'prompt': 'This video was shot in Japan. Please describe the situation on the screen as concisely as possible.',
        'images': [base64_image]
    }

    response = requests.post('http://localhost:11434/api/generate',
                            headers={'Content-Type': 'application/json'},
                            json=data,
                            stream=True)

    if response.status_code == 200:
        full_response = ''
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                if 'response' in json_response:
                    full_response += json_response['response']
                    print(json_response['response'], end='', flush=True)
                if json_response.get('done', False):
                    break
        return full_response
    else:
        return f"Error: {response.status_code} - {response.text}"

# 画像分析を行うエンドポイント(いまは、prossece_videoからのPOSTを想定)
@video_processing_blueprint.route("/analyze_images", methods=["POST"])
def analyze_images():
    try:
        transcription = request.json.get("transcription", "")
        image_paths = request.json.get("image_paths", [])
        
        if not transcription:
            return jsonify({"error": "文字起こし結果がありません"}), 400
        
        if not image_paths:
            return jsonify({"error": "画像パスがありません"}), 400

        analysis_results = []
        for idx, image_path in enumerate(image_paths):
            if not os.path.exists(image_path):
                continue
            ollama_result = analyze_image_with_ollama(image_path)
            analysis_results.append(f"{idx+1}秒: {ollama_result}")

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

        print(openai.api_key)  # APIキーを確認
        openai_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
            {"role": "system", "content": "画像の分析結果・音声の文字起こしの結果について、添付された日本の法律についてのJsonファイルから、違反していそうな法律のID・法律名・今回の結果について法律の違反確率を1~10段階評価・なぜそう思ったか・その他のリスクについて、以下の様式にしたがってレスポンスを返してください。"},
            {"role": "system", "content": """
            {
                "laws": [
                    {
                        "law_id": "法律のID", # int
                        "law_name": "法律名",  # str
                        "law_risk_level": "法律の違反確率", # int(0~10) 
                        "law_reason": "なぜそう思ったか" #str
                    }
                ], 
                "comment": "その他のリスクについて", #str
                "rating": "1~10段階評価によるリスク評価" #int(0~10)
            }
            """},
            {"role": "user", "content": summary_prompt},
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


"""
------------------------------------------------------------------
    以下、Blueskyのエンドポイント
------------------------------------------------------------------
"""

@bluesky_blueprint.route("/bluesky_gettimeline", methods=["GET"])
def bluesky_gettimeline():
    try:
        res = client.get_timeline()
        # Extract feed data from response and convert each post to dict
        feed_data = [post.dict() for post in res.feed]
        return jsonify({"feed": feed_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bluesky_blueprint.route("/bluesky_getprofile/<handle>", methods=["GET"])
def bluesky_getprofile(handle):
    try:
        # Get profile data using the provided handle
        profile = client.get_profile(handle)
        # Convert profile data to dict
        profile_data = profile.dict()
        return jsonify({"profile": profile_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bluesky_blueprint.route("/bluesky_post_video", methods=["POST"])
def post_video():
    try:
        # フォームからデータを取得
        text = request.form.get("text")
        video_file = request.files.get("video")

        # バリデーション
        if not text:
            return jsonify({"status": "error", "message": "no_test"}), 400
        if not video_file:
            return jsonify({"status": "error", "message": "no_video_files"}), 400

        # 動画データの読み込み
        video_data = video_file.read()

        # 動画投稿
        response = client.send_video(
            text=text,
            video=video_data,
            video_alt="動画の説明文"
        )
        
        return jsonify({
            "status": "success",
            "message": "投稿が完了しました"
        }), 200

    except Exception as e:
        print(f"動画投稿エラー: {e}")
        return jsonify({
            "status": "error", 
            "message": f"投稿に失敗しました: {str(e)}"
        }), 500
