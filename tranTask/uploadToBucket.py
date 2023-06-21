from google.cloud import storage
from tkinter import filedialog
import os

def check_file_exists(bucket_name, file_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    return blob.exists()

def upload_file_to_bucket(bucket_name, file_path, key_file):
    storage_client = storage.Client.from_service_account_json(key_file)
    bucket = storage_client.get_bucket(bucket_name)
    file_name = os.path.basename(file_path)
    blob = bucket.blob(file_name)
    file_exists = check_file_exists(bucket_name, file_name)
    if file_exists:
        print(f"The file '{file_name}' already exists.")
    else:
        blob.upload_from_filename(file_path)

    # 取得上傳後的檔案 URL
    file_url = blob.public_url
    return file_url

if __name__ == "__main__":
    bucket_name = "haku-trans-bucket"
    file_path = filedialog.askopenfilename()
    key_file = filedialog.askopenfilename()

    file_url = upload_file_to_bucket(bucket_name, file_path, key_file)
    print("上傳後的檔案 URL:", file_url)

    