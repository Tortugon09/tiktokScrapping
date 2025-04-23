import asyncio
from scraper.hashtag_example import get_hashtag_videos
from storage.database import init_db, save_videos

async def main():
    init_db()
    hashtag = "snackscolombia"
    videos = await get_hashtag_videos(hashtag, count=5)
    save_videos(videos)

if __name__ == "__main__":
    asyncio.run(main())
