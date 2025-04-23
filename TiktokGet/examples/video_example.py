from TikTokApi import TikTokApi
import asyncio
import os

ms_token = os.environ.get(
    "xj5Ii82tVCA1ISkvI65EJTlNvIGHz8iwrocK23SQNZMLvjmK5YQn5ONKZhYPztMvYUtcMKkRCggfrR1WwTaO7bDK7jH4fqfogBjOsB9bTDuBgvhOBt_5Q9UMEno1MICUpM5JSRFgSLXz4A==", None
)  # set your own ms_token, think it might need to have visited a profile

proxies = [
    {"server": "http://38.153.152.244:9594", "username": "mawbeuvu", "password": "5rqx9ch89vii"},
    {"server": "http://86.38.234.176:6630", "username": "mawbeuvu", "password": "5rqx9ch89vii"},
    {"server": "http://173.211.0.148:6641", "username": "mawbeuvu", "password": "5rqx9ch89vii"},
    {"server": "http://161.123.152.115:6360", "username": "mawbeuvu", "password": "5rqx9ch89vii"},
    {"server": "http://216.10.27.159:6837", "username": "mawbeuvu", "password": "5rqx9ch89vii"},
    {"server": "http://154.36.110.199:6853", "username": "mawbeuvu", "password": "5rqx9ch89vii"},
    {"server": "http://45.151.162.198:6600", "username": "mawbeuvu", "password": "5rqx9ch89vii"},
    {"server": "http://185.199.229.156:7492", "username": "mawbeuvu", "password": "5rqx9ch89vii"},
    {"server": "http://185.199.228.220:7300", "username": "mawbeuvu", "password": "5rqx9ch89vii"},
    {"server": "http://185.199.231.45:8382", "username": "mawbeuvu", "password": "5rqx9ch89vii"}
]

async def get_video_example():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, browser=os.getenv("TIKTOK_BROWSER", "chromium"), proxies=proxies, timeout=60000)
        video = api.video(
            url="https://www.tiktok.com/@thrivingonplants/video/7415964680537066760"
        )
        video_info = await video.info()  # is HTML request, so avoid using this too much
        print(video_info)
        video_bytes = await video.bytes()
        with open("video.mp4", "wb") as f:
            f.write(video_bytes)


if __name__ == "__main__":
    asyncio.run(get_video_example())
