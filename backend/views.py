from flask import Blueprint, jsonify, request
import cv2
from os import makedirs
from os.path import splitext, basename, join

video_processing_blueprint = Blueprint("video_processing", __name__)

# 動画からフレームを保存するエンドポイント
@video_processing_blueprint.route("/process_video", methods=["POST"])
def process_video():
    # フロントエンドから送信されたファイルを取得
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "ファイルがありません"}), 400

    # ファイルを一時保存する
    video_path = join("backend/video", file.filename)
    file.save(video_path)

    # フレームを保存
    frame_dir = "backend/frame"
    save_frames(video_path, frame_dir)

    # 成功メッセージを返す
    return jsonify({"message": "フレームが保存されました", "frame_directory": frame_dir})

def save_frames(video_path: str, frame_dir: str, name="image", ext="jpg"):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # 動画の基本情報を取得
    fps = cap.get(cv2.CAP_PROP_FPS)  # フレームレート
    v_name = splitext(basename(video_path))[0]
    frame_dir = join(frame_dir, v_name)

    # フレーム保存先ディレクトリを作成
    makedirs(frame_dir, exist_ok=True)
    base_path = join(frame_dir, name)

    idx = 0
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 1秒ごとにフレームを保存
        if frame_count % int(fps) == 0:  # フレームレートごとに1秒分のフレーム
            filled_idx = str(idx).zfill(4)  # ゼロ埋めでファイル名を作成
            cv2.imwrite(f"{base_path}_{filled_idx}.{ext}", frame)
            idx += 1

        frame_count += 1

    cap.release()
    print(f"Frames have been saved in {frame_dir}")
