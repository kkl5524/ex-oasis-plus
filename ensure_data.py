import os
import zipfile
import requests
from requests.adapters import HTTPAdapter, Retry
import gdown

def ensure_dir_for_file(path):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)

def download_from_drive(file_id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)

    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value

    if token:
        response = session.get(URL, params={'id': file_id, 'confirm': token}, stream=True)

    ensure_dir_for_file(destination)
    
    total = int(response.headers.get('content-length', 0))
    downloaded = 0
    chunk_size = 1024 * 64

    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    percent = downloaded / total * 100
                    print(f"\rDownloaded: {percent:5.1f}% ({downloaded/1e6:.1f} MB / {total/1e6:.1f} MB)", end="")
                else:
                    print(f"\rDownloaded: {downloaded/1e6:.1f} MB", end="")
    print("\nDownload complete.")

# 1. Download Synthea JAR
JAR_FILE_ID = "1IPmJdCrfkxoY0aydEZZ2vYZHOWh4AdzA"
JAR_PATH = "synthea/synthea-with-dependencies.jar"
JAR_DIR = "synthea"

def ensure_synthea_jar():
    if os.path.exists(JAR_PATH):
        print("synthea jar directory already exists.")
        return
    
    print("\nDownloading synthea-with-dependencies.jar from Google Drive...")
    ensure_dir_for_file(JAR_PATH)
    gdown.download(f"https://drive.google.com/uc?id={JAR_FILE_ID}", JAR_PATH, quiet=False)
    print("\nSynthea JAR download complete.")

# 2. Download mimic_demo.zip
MIM_DEMO_FILE_ID = "1xGcpnLzkdewGWs_vojoE8vE3v-U90A8t"
MIM_DEMO_ZIP = "mimic_demo.zip"
MIM_DEMO_DIR = "mimic_demo"

def ensure_mimic_demo_zip():
    if os.path.exists(MIM_DEMO_DIR):
        print("mimic_demo directory already exists.")
        return

    print("\nDownloading mimic_demo.zip from Google Drive...")
    ensure_dir_for_file(MIM_DEMO_ZIP)
    gdown.download(f"https://drive.google.com/uc?id={MIM_DEMO_FILE_ID}", MIM_DEMO_ZIP, quiet=False)

    print("Extracting mimic_demo.zip...")
    os.makedirs(MIM_DEMO_DIR, exist_ok=True)
    with zipfile.ZipFile(MIM_DEMO_ZIP, 'r') as z:
        z.extractall(MIM_DEMO_DIR)
    print("Extraction complete.")

    os.remove(MIM_DEMO_ZIP)
    print("Cleaned up mimic_demo.zip")

# 3. Download synthea_output.zip
SYN_OUT_FILE_ID = "1a9P6FhM12T8NZ_XYfOdft0Gn77CuyPs7"
SYN_OUT_ZIP = "output/synthea_output.zip"
SYN_OUT_DIR = "output/synthea_output"

def ensure_synthea_output_zip():
    if os.path.exists(SYN_OUT_DIR):
        print("synthea_output directory already exists.")
        return

    print("\nDownloading synthea_output.zip from Google Drive...")
    ensure_dir_for_file(SYN_OUT_ZIP)
    gdown.download(f"https://drive.google.com/uc?id={SYN_OUT_FILE_ID}", SYN_OUT_ZIP, quiet=False)

    print("Extracting synthea_output.zip...")
    os.makedirs(SYN_OUT_DIR, exist_ok=True)
    with zipfile.ZipFile(SYN_OUT_ZIP, 'r') as z:
        z.extractall(SYN_OUT_DIR)
    print("Extraction complete.")

    os.remove(SYN_OUT_ZIP)
    print("Cleaned up synthea_output.zip")

# Run everything
def ensure_all_data():
    try:
        ensure_synthea_jar()
    except Exception as e:
        print(f"Warning: Could not download Synthea JAR: {e}")

    try:
        ensure_mimic_demo_zip()
    except Exception as e:
        print(f"Warning: Could not download mimic_demo: {e}")

    try:
        ensure_synthea_output_zip()
    except Exception as e:
        print(f"Warning: Could not download synthea_output: {e}")

ensure_all_data()
