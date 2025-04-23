from TikTokApi import TikTokApi
import asyncio
import os
import json
import yt_dlp
import requests
from bs4 import BeautifulSoup
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import time
import firebase_admin
from firebase_admin import credentials, storage
import io
from scraper.downloader  import TikTokDownloader

# 🔐 Inicializa Firebase solo una vez
import firebase_admin
from firebase_admin import credentials, storage
import io
import os

assert os.path.exists("key")
cred = credentials.Certificate("key")
try:
    firebase_admin.initialize_app(cred, {
        'storageBucket': '#buvket'
    })
    print("Firebase app initialized successfully!")
except Exception as e:
    print(f"Error initializing Firebase app: {e}")

async def subir_video_a_firebase(video_id):
    try:
        video_bytes = await video_id.bytes()

        # Usa un buffer en memoria
        file_stream = io.BytesIO(video_bytes)

        # Define nombre en el storage
        nombre_archivo = f"video_{video_id.id}.mp4"

        # Subida al bucket
        bucket = storage.bucket(app=firebase_admin.get_app()) #Explicitly pass the app instance
        blob = bucket.blob(nombre_archivo)
        blob.upload_from_file(file_stream, content_type='video/mp4')

        # Opcional: hacerlo público
        blob.make_public()

        print("✅ Video subido:", blob.public_url)
        return blob.public_url
    except Exception as e:
        print(f"❌ Error uploading video: {e}")
        return None

ms_token = os.environ.get("xj5Ii82tVCA1ISkvI65EJTlNvIGHz8iwrocK23SQNZMLvjmK5YQn5ONKZhYPztMvYUtcMKkRCggfrR1WwTaO7bDK7jH4fqfogBjOsB9bTDuBgvhOBt_5Q9UMEno1MICUpM5JSRFgSLXz4A==", None)  # set your own ms_token
proxies = [
    {"server": "http://38.153.152.244:9594", "username": "hnxnoyiu", "password": "trbwt4yuq8dp"},
    {"server": "http://86.38.234.176:6630", "username": "hnxnoyiu", "password": "trbwt4yuq8dp"},
    {"server": "http://173.211.0.148:6641", "username": "hnxnoyiu", "password": "trbwt4yuq8dp"},
    {"server": "http://161.123.152.115:6360", "username": "hnxnoyiu", "password": "trbwt4yuq8dp"},
    {"server": "http://216.10.27.159:6837", "username": "hnxnoyiu", "password": "trbwt4yuq8dp"},
    {"server": "http://154.36.110.199:6853", "username": "hnxnoyiu", "password": "trbwt4yuq8dp"},
    {"server": "http://45.151.162.198:6600", "username": "hnxnoyiu", "password": "trbwt4yuq8dp"},
    {"server": "http://185.199.229.156:7492", "username": "hnxnoyiu", "password": "trbwt4yuq8dp"},
    {"server": "http://185.199.228.220:7300", "username": "hnxnoyiu", "password": "trbwt4yuq8dp"},
    {"server": "http://185.199.231.45:8382", "username": "hnxnoyiu", "password": "trbwt4yuq8dp"}
]

from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
import time

def obtener_url_video_tiktok(tiktok_url):
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0")

    # Usamos el driver de Edge
    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)

    driver.get(tiktok_url)
    time.sleep(5)

    try:
        # Buscamos la etiqueta <source> dentro del <video>
        source_element = driver.find_element("tag name", "source")
        video_url = source_element.get_attribute("src")
        print(f"🎯 Video URL encontrado: {video_url}")
    except Exception as e:
        print(f"❌ No se pudo encontrar el video: {e}")
        video_url = None

    driver.quit()
    return video_url

def descargar_video(url_video, nombre_archivo="video_descargado.mp4"):
    response = requests.get(url_video, stream=True)
    if response.status_code == 200:
        with open(nombre_archivo, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"✅ Video descargado como {nombre_archivo}")
    else:
        print("❌ Error al descargar el video")

async def get_hashtag_videos(hashtag: str, count: int = 30):
    async with TikTokApi() as api:
        await api.create_sessions(
            ms_tokens=[ms_token],
            headless=False,
            num_sessions=1,
            sleep_after=3,
            browser=os.getenv("TIKTOK_BROWSER", "chromium"),
            timeout=60000,
            proxies=proxies
        )

        video_data = []
        tag = api.hashtag(name=hashtag)
        async for video in tag.videos(count):
            print(video.author.username)
            print(video.id)
            print(video.stats)
            if video.author.username is not None and video.id is not None:
                url=f"https://www.tiktok.com/@{video.author.username}/video/{video.id}"

                video_id = api.video(url=url)
                try:
                    video_info = await video_id.info()
                    print(video_info["desc"])
                    video_bytes = await video_id.bytes()
                    url_download = await subir_video_a_firebase(video_id)
                    print(url_download)
                    data = {
                    "id": str(video.id),
                    "description": video_info["desc"],
                    "likes": int(video.stats["diggCount"]),
                    "author": str(video.author.username),
                    "comments": int(video.stats["commentCount"]),
                    "video_url": f"{url_download}",
                    "playCount": int(video.stats["playCount"]),
                    "comments_list": []
                    }
                    video_data.append(data)
                except Exception as e:
                    print(f"Error procesando video {video.id}: {e}")
                    continue
        return video_data
    
if __name__ == "__main__":
    asyncio.run(get_hashtag_videos())
