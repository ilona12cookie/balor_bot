import asyncio
import telegram


async def main():
    bot = telegram.Bot("8538713738:AAFtqH9O6DBQ7kXB8AzfyOq9F7M2iamgFpg")
    async with bot:
        print(await bot.get_me())


if __name__ == '__main__':
    asyncio.run(main())
