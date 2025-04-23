from TikTokApi import TikTokApi
import asyncio
import os
import json

ms_token = os.environ.get("xj5Ii82tVCA1ISkvI65EJTlNvIGHz8iwrocK23SQNZMLvjmK5YQn5ONKZhYPztMvYUtcMKkRCggfrR1WwTaO7bDK7jH4fqfogBjOsB9bTDuBgvhOBt_5Q9UMEno1MICUpM5JSRFgSLXz4A==", None)  # set your own ms_token

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

async def get_hashtag_videos():
    async with TikTokApi() as api:
        await api.create_sessions(
            ms_tokens=[ms_token],
            headless=False,
            num_sessions=1,
            sleep_after=3,
            browser=os.getenv("TIKTOK_BROWSER", "chromium"),
            proxies=proxies,
            timeout=60000
        )


        tag = api.hashtag(name="snacks")
        async for video in tag.videos(count=30):
            print(video.author.username)
            print(video.id)
            if video.author.username is not None and video.id is not None:
                video_id = api.video(url=f"https://www.tiktok.com/@{video.author.username}/video/{video.id}")
                try:
                    video_info = await video_id.info()
                    print(video_info)
                    video_bytes = await video_id.bytes()
                    with open(f"video{video.id}.mp4", "wb") as f:
                        f.write(video_bytes)
                except:
                    continue


if __name__ == "__main__":
    asyncio.run(get_hashtag_videos())
