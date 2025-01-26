import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import API_TOKEN
from handlers import start, handle_callback, search_recipes, handle_recipe_callback, handle_favorite
from middlewares import BotMiddleware

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.message.register(start, Command("start"))
dp.callback_query.register(handle_callback, F.data.in_({"search", "favorites", "viewed", "back", "clear_history"}))
dp.message.register(search_recipes, F.text)
dp.callback_query.register(handle_recipe_callback, F.data.startswith("recipe_"))
dp.callback_query.register(handle_favorite, F.data.startswith("add_favorite_") | F.data.startswith("remove_favorite_"))

async def main():
    dp.update.middleware(BotMiddleware(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())