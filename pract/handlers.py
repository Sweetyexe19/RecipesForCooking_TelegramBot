from aiogram import types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data import favorites, viewed, save_data, FAVORITES_FILE, VIEWED_FILE
from utils import create_main_menu, show_recipes_list, search_recipes_by_ingredient, get_recipe_by_id, send_recipe


async def start(message: types.Message):
    await message.answer("🍴 Добро пожаловать! Выберите действие:", reply_markup=create_main_menu())


async def handle_callback(callback: types.CallbackQuery):
    user_id = str(callback.from_user.id)

    if callback.data == "search":
        await callback.message.answer("🔍 Введите ингредиент \n"
                                      " ❗️ На Английском:")
    elif callback.data == "favorites":
        if user_id in favorites and favorites[user_id]:
            await show_recipes_list(callback, favorites[user_id], "⭐ Избранное:")
        else:
            await callback.message.answer("⭐ Нет избранных рецептов.")
    elif callback.data == "viewed":
        if user_id in viewed and viewed[user_id]:
            await show_recipes_list(callback, viewed[user_id], "📚 Просмотренные:")
        else:
            await callback.message.answer("📚 История пуста.")
    elif callback.data == "back":
        await callback.message.answer("🍴 Главное меню:", reply_markup=create_main_menu())
    elif callback.data == "clear_history":
        if user_id in viewed:
            viewed[user_id] = []
            save_data(VIEWED_FILE, viewed)
            await callback.answer("🧹 История очищена!")
        else:
            await callback.answer("📚 Нет истории.")


async def search_recipes(message: types.Message):
    user_id = str(message.from_user.id)
    ingredient = message.text.lower()

    recipes = await search_recipes_by_ingredient(ingredient, user_id)
    if not recipes:
        await message.answer("❌ Рецепты не найдены")
        return

    builder = InlineKeyboardBuilder()
    for recipe in recipes:
        builder.add(InlineKeyboardButton(text=recipe["title"], callback_data=f"recipe_{recipe['id']}"))
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="back"))
    await message.answer("🍴 Результаты поиска:", reply_markup=builder.as_markup())


async def handle_recipe_callback(callback: types.CallbackQuery, bot):
    user_id = str(callback.from_user.id)
    recipe_id = callback.data.split("_")[1]

    if user_id not in viewed:
        viewed[user_id] = []
    if recipe_id not in viewed[user_id]:
        viewed[user_id].append(recipe_id)
        save_data(VIEWED_FILE, viewed)

    recipe = await get_recipe_by_id(recipe_id)
    if recipe:
        await send_recipe(bot, callback.message.chat.id, recipe)
        builder = InlineKeyboardBuilder()
        if user_id in favorites and recipe_id in favorites[user_id]:
            builder.add(InlineKeyboardButton(text="❌ Удалить", callback_data=f"remove_favorite_{recipe_id}"))
        else:
            builder.add(InlineKeyboardButton(text="⭐ В избранное", callback_data=f"add_favorite_{recipe_id}"))
        builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="back"))
        await callback.message.answer("Действие:", reply_markup=builder.as_markup())
    else:
        await callback.message.answer("❌ Ошибка загрузки")
    await callback.message.edit_reply_markup(reply_markup=None)


async def handle_favorite(callback: types.CallbackQuery):
    user_id = str(callback.from_user.id)
    recipe_id = callback.data.split("_")[2]

    if user_id not in favorites:
        favorites[user_id] = []

    if callback.data.startswith("add_favorite_"):
        if recipe_id not in favorites[user_id]:
            favorites[user_id].append(recipe_id)
            await callback.answer("⭐ Добавлено!")
    else:
        if recipe_id in favorites[user_id]:
            favorites[user_id].remove(recipe_id)
            await callback.answer("❌ Удалено!")
    save_data(FAVORITES_FILE, favorites)