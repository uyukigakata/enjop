from dotenv import load_dotenv
import os
from google.cloud import speech

# .envファイルの内容を読み込む
load_dotenv()

# Speech-to-Textクライアントの初期化
client = speech.SpeechClient()

# 音声ファイルをテキストに変換する関数
def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # 音声ファイルのエンコーディングを指定
        sample_rate_hertz=16000,  # サンプルレートを指定
        language_code="ja-JP"  # 日本語を指定
    )

    # 音声をテキストに変換するリクエストを送信
    response = client.recognize(config=config, audio=audio)

    # 結果を出力
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

# 音声ファイルのパスを指定
transcribe_audio("C:/Users/yuu/Document/prpduct/SeckHack/SecHack365_4C_enjo/API/movie/oden.mp4")
