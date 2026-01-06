#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ГЛАВНЫЙ ФАЙЛ ЗАПУСКА БОТА БАЛОРА
Владыка Проклятого Взгляда | Бесобой
"""

import logging
from telegram.ext import Application

# Импорт наших модулей
from config import BOT_TOKEN, BOT_CONFIG, LOGGING_CONFIG, validate_config
from handlers import register_handlers

# ===================== НАСТРОЙКА ЛОГГИРОВАНИЯ =====================
logging.basicConfig(
    format=LOGGING_CONFIG["format"],
    level=getattr(logging, LOGGING_CONFIG["level"]),
)

logger = logging.getLogger(__name__)

# ===================== ФУНКЦИЯ ЗАПУСКА =====================
def main():
    """Основная функция запуска бота"""
    try:
        # Проверяем конфигурацию
        print("=" * 60)
        print("👁️  ЗАПУСК БОТА БАЛОРА - ВЛАДЫКА ПРОКЛЯТОГО ВЗГЛЯДА")
        print("=" * 60)
        
        validate_config()
        
        # Создаём приложение
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Регистрируем обработчики
        application = register_handlers(application)
        
        # Выводим информацию о боте
        print("\n📊 ИНФОРМАЦИЯ О БОТЕ:")
        print(f"   • Имя: {BOT_CONFIG['name']}")
        print(f"   • Версия: {BOT_CONFIG['version']}")
        print(f"   • Разработчик: {BOT_CONFIG['developer']}")
        print(f"   • Описание: {BOT_CONFIG['description']}")
        
        # Импортируем статистику баз данных
        from lore_database import get_lore_statistics
        from curses_database import get_curses_statistics
        
        lore_stats = get_lore_statistics()
        curse_stats = get_curses_statistics()
        
        print("\n📚 БАЗЫ ДАННЫХ:")
        print(f"   • Частей истории: {lore_stats['lore_parts']}")
        print(f"   • Цитат мудрости: {lore_stats['quotes']}")
        print(f"   • Проклятий: {curse_stats['total_curses']}")
        print(f"   • Уровней проклятий: {len(curse_stats['by_tier'])}")
        
        print("\n🔗 ССЫЛКИ:")
        print(f"   • Бот: https://t.me/{BOT_TOKEN.split(':')[0]}_bot")
        print(f"   • Лог-файл: {LOGGING_CONFIG['file']}")
        
        print("\n" + "=" * 60)
        print("✅ Бот запускается... (остановить: Ctrl+C)")
        print("=" * 60)
        
        # Запускаем бота
        application.run_polling(allowed_updates=[])
        
    except ValueError as e:
        print(f"\n❌ ОШИБКА КОНФИГУРАЦИИ: {e}")
        print("\n🔧 КАК ИСПРАВИТЬ:")
        print("1. Создай файл .env в корне проекта")
        print("2. Добавь строку: BOT_TOKEN=твой_токен_от_BotFather")
        print("3. Перезапусти бота")
        
    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        logger.exception("Ошибка при запуске бота:")
        
    finally:
        print("\n" + "=" * 60)
        print("👁️  Бот Балор завершил работу")
        print("=" * 60)

# ===================== ТОЧКА ВХОДА =====================
if __name__ == "__main__":
    main()
