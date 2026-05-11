import asyncio


async def start_scheduler():
    while True:
        await asyncio.sleep(5)