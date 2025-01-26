from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import SPOONACULAR_API_KEY
from data import viewed
import aiohttp


def create_main_menu():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🔍 Поиск", callback_data="search"),
        InlineKeyboardButton(text="⭐ Избранное", callback_data="favorites"),
        InlineKeyboardButton(text="📚 История", callback_data="viewed")
    )
    builder.adjust(1)
    return builder.as_markup()


async def show_recipes_list(callback, recipe_ids, title):
    builder = InlineKeyboardBuilder()
    for recipe_id in recipe_ids:
        recipe = await get_recipe_by_id(recipe_id)
        if recipe:
            builder.add(InlineKeyboardButton(text=recipe["title"], callback_data=f"recipe_{recipe_id}"))
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="🧹 Очистить", callback_data="clear_history"))
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="back"))
    await callback.message.answer(title, reply_markup=builder.as_markup())


async def search_recipes_by_ingredient(ingredient, user_id):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ingredient,
        "apiKey": SPOONACULAR_API_KEY,
        "number": 10
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                if user_id in viewed:
                    return [r for r in data if str(r["id"]) not in viewed[user_id]]
                return data
            return None


async def get_recipe_by_id(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "includeNutrition": "false"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                return await resp.json()
            return None


async def send_recipe(bot, chat_id, recipe):
    try:
        image_url = recipe['image']
    except KeyError:
        image_url = None

    response = f"🍴 <b>{recipe['title']}</b>\n\n"
    response += "📝 <b>Ингредиенты:</b>\n"
    for ingredient in recipe["extendedIngredients"]:
        response += f"- {ingredient['original']}\n"

    response += "\n📖 <b>Инструкции:</b>\n"
    instructions = recipe.get("instructions", "")
    if instructions:
        instructions = instructions.replace("<ol>", "").replace("</ol>", "").replace("<li>", "• ").replace("</li>",
                                                                                                           "\n")
        response += instructions
    else:
        response += "Инструкции отсутствуют."

    if image_url:
        await bot.send_photo(
            chat_id=chat_id,
            photo=image_url,
            caption=response,
            parse_mode="HTML"
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=response,
            parse_mode="HTML"
        )