from TikTokApi import TikTokApi
import asyncio
import os

ms_token = os.environ.get(
    "xj5Ii82tVCA1ISkvI65EJTlNvIGHz8iwrocK23SQNZMLvjmK5YQn5ONKZhYPztMvYUtcMKkRCggfrR1WwTaO7bDK7jH4fqfogBjOsB9bTDuBgvhOBt_5Q9UMEno1MICUpM5JSRFgSLXz4A==", None
)  # set your own ms_token, needs to have done a search before for this to work


async def search_users():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, browser=os.getenv("TIKTOK_BROWSER", "chromium"))
        async for user in api.search.users("llados", count=10):
            print(user)


if __name__ == "__main__":
    asyncio.run(search_users())
