import tkinter as tk
from tkinter import filedialog
from google.cloud import speech_v1p1beta1  as speech

audio_path = None
auth_path = None


def get_audio_path():
    tmp_filepath = filedialog.askopenfilename()
    if tmp_filepath != "":
        global audio_path 
        audio_path = tmp_filepath

def get_auth_path():
    tmp_filepath = filedialog.askopenfilename()
    if tmp_filepath != "":
        global auth_path 
        auth_path = tmp_filepath

def transcribe_speech(audio_path, auth_path):

    if audio_path is not None and auth_path is not None:
        credentials_file = auth_path
        if credentials_file:
            client = speech.SpeechClient.from_service_account_json(credentials_file)

            # 讀取音訊檔案
            with open(audio_path, "rb") as audio_file:
                content = audio_file.read()

            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding="MP3",
                sample_rate_hertz=16000,
                language_code="ja-JP",
            )

            # 呼叫 Speech-to-Text API 進行語音轉換
            response = client.recognize(config=config, audio=audio)

            # 輸出辨識結果
            for result in response.results:
                print("辨識結果: {}".format(result.alternatives[0].transcript))


# 建立視窗
window = tk.Tk()

# 建立按鈕
button = tk.Button(window, text="選擇音訊檔案", command=get_audio_path)
button2 = tk.Button(window, text="選擇金鑰檔案", command=get_auth_path)
button3 = tk.Button(window, text="開始轉換", command=lambda: transcribe_speech(audio_path, auth_path))
button.pack()
button2.pack()
button3.pack()

# 開始事件迴圈
window.mainloop()