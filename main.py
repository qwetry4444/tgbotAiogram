import asyncio
from db import db
import message_handler
from aiogram import executor
from loader import dp
import middlwares



async def start():
    await executor.start_polling(dp, skip_updates=True)
#
#
#
# async def uptime():
#     while True:
#         print("UUUUUUUUUUP!")
#         asyncio.sleep(2)

async def uptimedb():
    while True:
        await db.wakeup()
        await asyncio.sleep(20)

async def main():

    await start()
    await uptimedb()

    # f1 = loop.create_task(start())
    # f2 = loop.create_task(uptimedb())
    #
    # await asyncio.wait([f1, f2])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)