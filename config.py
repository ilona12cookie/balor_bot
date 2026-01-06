#!/usr/bin/env python3
"""
Конфигурация бота Балор
"""

import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Токен бота
BOT_TOKEN = "8538713738:AAFtqH9O6DBQ7kXB8AzfyOq9F7M2iamgFpg"

# Настройки бота
BOT_CONFIG = {
    "name": "Балор - Владыка Проклятого Взгляда",
    "username": "BalorDemonBot",
    "version": "2.0.0",
    "description": "Демонический помощник из вселенной Бесобоя",
    "developer": "@твой_юзернейм",
}

# Настройки логирования
LOGGING_CONFIG = {
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "level": "INFO",
    "file": "balor.log",
}

# Проверка конфигурации
def validate_config():
    """Проверка корректности конфигурации"""
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN не найден! Добавьте его в .env файл")
    
    if len(BOT_TOKEN) < 30:
        raise ValueError("❌ Неверный формат BOT_TOKEN")
    
    print("✅ Конфигурация загружена успешно")
    print(f"📛 Имя бота: {BOT_CONFIG['name']}")
    print(f"🆔 Версия: {BOT_CONFIG['version']}")
    
    return True
