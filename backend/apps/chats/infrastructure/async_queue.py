import asyncio


def fire_and_forget(coro):
    asyncio.create_task(coro)