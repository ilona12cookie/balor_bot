#!/usr/bin/env python3
"""
Обработчики команд для бота Балор
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, Any

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from lore_database import get_lore_part, BALOR_QUOTES
from curses_database import get_random_curse, format_curse_display, get_curses_statistics, CURSE_SYSTEM
from utils import TextFormatter, CurseAnimator, AchievementSystem, get_keyword_response, get_random_response

# Глобальные системы
achievement_system = AchievementSystem()

# ===================== ОСНОВНЫЕ КОМАНДЫ =====================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    
    # Сохраняем время старта в контекст
    if 'start_time' not in context.bot_data:
        context.bot_data['start_time'] = datetime.now()
    
    text = f"""
👁️ <b>БАЛОР ПРОБУЖДЁН</b>

<i>«{random.choice(['Твой звонок разбудил меня от векового сна.', 
                  'Давно не слышал зова смертных.', 
                  'Ты знаешь, с кем говоришь?'])}»</i>

<b>{user.first_name}</b>, приветствую тебя в моей цифровой обители.

Я — Балор. Владыка Проклятого Взгляда. Бесобой.
Существо баланса, хранитель равновесия между светом и тьмой.

<b>Что я могу:</b>
• Рассказать о себе (/lore)
• Наложить проклятие (/curse или /curse_roulette)
• Изречь мудрость (/quote)
• Показать статус (/status)
• И многое другое (/help)

<i>Выбирай команду. Я слушаю.</i>

<code>Версия 2.0 | Демонический код активен</code>
"""
    
    # Клавиатура с основными командами
    keyboard = [
        ["/lore", "/quote"],
        ["/curse", "/curse_roulette"],
        ["/status", "/help"]
    ]
    
    await update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    
    # Логирование
    print(f"👤 Пользователь {user.username or user.first_name} запустил бота")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    commands = {
        "start": "Пробудить Балор",
        "help": "Помощь и команды",
        "lore": "Легенда о Балор (8 частей)",
        "quote": "Мудрость Балора (100+ цитат)",
        "curse": "Простое проклятие",
        "curse_roulette": "Рулетка проклятий (5 уровней)",
        "curse_protect": "Попытка снять проклятие",
        "curse_stats": "Статистика проклятий",
        "status": "Статус Балора",
        "info": "Информация о боте"
    }
    
    text = TextFormatter.format_help(commands)
    await update.message.reply_html(text)

async def lore_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /lore"""
    lore_part = get_lore_part()
    
    # Обновляем статистику
    user_id = update.effective_user.id
    new_achievements = achievement_system.update_stats(user_id, "lore")
    
    text = f"""
{lore_part['title']}
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
{lore_part['content']}

<code>Часть {lore_part['order']} из 8 | Всего частей: 8</code>
<i>Используй /lore снова, чтобы узнать больше</i>
"""
    
    await update.message.reply_html(text)
    
    # Проверяем достижения
    if new_achievements:
        for achievement in new_achievements:
            achievement_text = f"""
{achievement['emoji']} <b>НОВОЕ ДОСТИЖЕНИЕ!</b>

🏆 <b>{achievement['name']}</b>
📝 {achievement['description']}

<code>Продолжай узнавать историю Балора</code>
"""
            await update.message.reply_html(achievement_text)

async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /quote"""
    quote_index = random.randrange(len(BALOR_QUOTES))
    quote = BALOR_QUOTES[quote_index]
    
    # Обновляем статистику
    user_id = update.effective_user.id
    new_achievements = achievement_system.update_stats(user_id, "quote")
    
    text = TextFormatter.format_quote(quote, quote_index, len(BALOR_QUOTES))
    await update.message.reply_html(text)
    
    # Проверяем достижения
    if new_achievements:
        for achievement in new_achievements:
            achievement_text = f"""
{achievement['emoji']} <b>НОВОЕ ДОСТИЖЕНИЕ!</b>

🏆 <b>{achievement['name']}</b>
📝 {achievement['description']}

<code>Продолжай собирать мудрость</code>
"""
            await update.message.reply_html(achievement_text)

# ===================== ПРОКЛЯТИЯ =====================
async def curse_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /curse - простое проклятие"""
    curse_data = get_random_curse()
    
    # Обновляем статистику
    user_id = update.effective_user.id
    new_achievements = achievement_system.update_stats(user_id, "curse", curse_data)
    
    text = format_curse_display(curse_data)
    await update.message.reply_html(text)
    
    # Проверяем достижения
    if new_achievements:
        for achievement in new_achievements:
            achievement_text = f"""
{achievement['emoji']} <b>НОВОЕ ДОСТИЖЕНИЕ!</b>

🏆 <b>{achievement['name']}</b>
📝 {achievement['description']}

<code>Будь осторожен с проклятиями</code>
"""
            await update.message.reply_html(achievement_text)

async def curse_roulette_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /curse_roulette - рулетка проклятий"""
    # Отправляем начальное сообщение
    message = await update.message.reply_text("🎡 *Запускаю рулетку проклятий...*", parse_mode='Markdown')
    
    # Анимация
    async def edit_msg(text):
        await message.edit_text(text, parse_mode='Markdown')
    
    await CurseAnimator.animate_roulette(message, edit_msg)
    
    # Выбираем проклятие
    curse_data = get_random_curse()
    
    # Обновляем статистику
    user_id = update.effective_user.id
    new_achievements = achievement_system.update_stats(user_id, "curse", curse_data)
    
    # Форматируем результат
    tier_info = curse_data["system"]
    category_name = CURSE_SYSTEM["CATEGORIES"].get(curse_data["category"], curse_data["category"])
    
    text = f"""
{tier_info['emoji']} <b>РУЛЕТКА ПРОКЛЯТИЙ</b>
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
🎰 <b>Результат:</b> {curse_data['tier']}
🔮 <b>Категория:</b> {category_name}
📝 <b>Проклятие:</b> {curse_data['text']} {curse_data['emoji']}

⚡ <b>Уровень:</b> {curse_data['tier']}
⏳ <b>Длительность:</b> {tier_info['duration']}
🛡️ <b>Шанс защиты:</b> {tier_info['protection_chance']}%
📊 <b>Вероятность:</b> {tier_info['weight']}%

<code>Используй /curse_protect для попытки снять</code>
"""
    
    await message.edit_text(text, parse_mode='HTML')
    
    # Проверяем достижения
    if new_achievements:
        for achievement in new_achievements:
            achievement_text = f"""
{achievement['emoji']} <b>НОВОЕ ДОСТИЖЕНИЕ!</b>

🏆 <b>{achievement['name']}</b>
📝 {achievement['description']}

<code>Рулетка судьбы улыбнулась тебе</code>
"""
            await update.message.reply_html(achievement_text)

async def curse_protect_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /curse_protect - защита от проклятий"""
    # Случайный результат
    success = random.random() < 0.33  # 33% шанс
    
    if success:
        text = """
🛡️ <b>ЗАЩИТА СРАБОТАЛА!</b>

Демоническая энергия рассеялась.
Проклятие снято... на время.

<i>Печать Балора светится на твоём запястье, затем гаснет.</i>

<code>Защита действует 24 часа</code>
"""
    else:
        text = """
❌ <b>ЗАЩИТА НЕ СРАБОТАЛА</b>

Проклятие сопротивляется.
Демоническая энергия слишком сильна.

<i>Печать треснула, но не сломалась.</i>

<code>Попробуй снова через час</code>
"""
    
    await update.message.reply_html(text)

async def curse_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /curse_stats - статистика проклятий"""
    stats = get_curses_statistics()
    user_stats = achievement_system.get_user_stats(update.effective_user.id)
    
    text = f"""
📊 <b>СТАТИСТИКА ПРОКЛЯТИЙ</b>
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

<b>Глобальная база:</b>
• Всего проклятий: {stats['total_curses']}
• Уровней редкости: {len(stats['by_tier'])}
• Категорий: {len(stats['by_category'])}
• Самый редкий уровень: {stats['strongest_tier']}

<b>По уровням:</b>
"""
    
    for tier, count in stats['by_tier'].items():
        percentage = (count / stats['total_curses'] * 100) if stats['total_curses'] > 0 else 0
        tier_emoji = CURSE_SYSTEM["TIERS"][tier]["emoji"]
        text += f"{tier_emoji} {tier}: {count} ({percentage:.1f}%)\n"
    
    text += f"\n<b>Твоя статистика:</b>\n"
    text += f"• Получено проклятий: {user_stats.get('curses_received', 0)}\n"
    text += f"• Уровней получено: {len(user_stats.get('tiers_received', set()))}/5\n"
    text += f"• Достижений: {len(user_stats.get('achievements', set()))}\n\n"
    
    text += "<i>Продолжай испытывать судьбу в /curse_roulette</i>\n\n"
    text += "<code>Знание — сила. Статистика — понимание.</code>"
    
    await update.message.reply_html(text)

# ===================== СТАТУС И ИНФО =====================
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /status"""
    start_time = context.bot_data.get('start_time', datetime.now())
    text = TextFormatter.format_status("БАЛОРА", start_time)
    await update.message.reply_html(text)

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /info - информация о боте"""
    from lore_database import get_lore_statistics
    from curses_database import get_curses_statistics
    
    lore_stats = get_lore_statistics()
    curse_stats = get_curses_statistics()
    
    text = f"""
ℹ️ <b>ИНФОРМАЦИЯ О БОТЕ</b>
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

<b>Основное:</b>
• Имя: Балор - Владыка Проклятого Взгляда
• Вселенная: Бесобой (Beso Boy)
• Тип: Бесобой (существо баланса)
• Статус: Цифровое воплощение

<b>Базы знаний:</b>
• Частей истории: {lore_stats['lore_parts']}
• Цитат мудрости: {lore_stats['quotes']}
• Проклятий: {curse_stats['total_curses']}
• Уровней проклятий: {len(curse_stats['by_tier'])}

<b>Техническое:</b>
• Версия: 2.0.0
• Архитектура: Модульная
• Язык: Python 3.10+
• Библиотека: python-telegram-bot
• Разработчик: {lore_stats['author']}

<b>Возможности:</b>
• Рассказ истории в 8 частях
• 100+ философских цитат
• Система проклятий с 5 уровнями редкости
• Интерактивная рулетка проклятий
• Система достижений
• Умные ответы на сообщения

<i>«Даже в коде есть душа. Особенно если код написан с душой.»</i>

<code>Обновлено: {lore_stats['last_updated']}</code>
"""
    
    await update.message.reply_html(text)

# ===================== ОБРАБОТЧИК ОБЫЧНЫХ СООБЩЕНИЙ =====================
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик обычных сообщений"""
    text = update.message.text
    
    # Пробуем получить ответ на ключевые слова
    response = get_keyword_response(text)
    
    # Если нет специального ответа, берём случайный
    if not response:
        response = get_random_response()
    
    await update.message.reply_text(response)

# ===================== РЕГИСТРАЦИЯ ОБРАБОТЧИКОВ =====================
def register_handlers(application):
    """Зарегистрировать все обработчики команд"""
    from telegram.ext import CommandHandler, MessageHandler, filters
    
    # Основные команды
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("lore", lore_command))
    application.add_handler(CommandHandler("quote", quote_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("info", info_command))
    
    # Проклятия
    application.add_handler(CommandHandler("curse", curse_command))
    application.add_handler(CommandHandler("curse_roulette", curse_roulette_command))
    application.add_handler(CommandHandler("curse_protect", curse_protect_command))
    application.add_handler(CommandHandler("curse_stats", curse_stats_command))
    
    # Обычные сообщения
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    return application
