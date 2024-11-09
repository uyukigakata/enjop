"Google Cloud Starageのfraeフォルダにアクセス"


from google.cloud import storage
from dotenv import load_dotenv
import os

# .envファイルの内容を読み込む
load_dotenv()

# Cloud Storageクライアントの初期化
client = storage.Client()
bucket_name = os.getenv("STORAGEBUCKET")  # .env からバケット名を取得
bucket = client.bucket(bucket_name)

# 特定のフォルダ（ここでは frame フォルダ）内のオブジェクトを取得
def list_files_in_frame_folder():
    blobs = bucket.list_blobs(prefix="frame/")  # frame フォルダ内のファイルを取得
    file_uris = [f"gs://{bucket_name}/{blob.name}" for blob in blobs if blob.name.endswith(".jpg")]

    return file_uris

# ファイルURIのリストを取得
frame_file_uris = list_files_in_frame_folder()
print("Frame フォルダ内のファイル:")
for uri in frame_file_uris:
    print(uri)
