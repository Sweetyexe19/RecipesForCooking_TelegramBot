from aiogram import Bot
from aiogram.types import TelegramObject
from aiogram.dispatcher.middlewares.base import BaseMiddleware

class BotMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def __call__(self, handler, event, data):
        data["bot"] = self.bot
        return await handler(event, data)