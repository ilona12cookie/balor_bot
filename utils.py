#!/usr/bin/env python3
"""
Вспомогательные утилиты для бота Балор
"""

import random
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any

# ===================== ФОРМАТТЕРЫ ТЕКСТА =====================
class TextFormatter:
    """Класс для форматирования текста"""
    
    @staticmethod
    def format_quote(quote: str, quote_number: int = None, total_quotes: int = None) -> str:
        """Форматировать цитату"""
        # Разделяем эмодзи и текст
        parts = quote.rsplit(' ', 1)
        if len(parts) > 1 and len(parts[1]) <= 5:  # Эмодзи обычно короткие
            text, emoji = parts[0], parts[1]
        else:
            text, emoji = quote, "🗣️"
        
        # Случайное вступление
        intros = [
            "Из глубины веков:",
            "Проклятый Взгляд видит:",
            "В демонических скрижалях:",
            "Балор когда-то сказал:",
            "Мудрость, которую я постиг:",
            "Из хроник Бесобоев:",
            "Истина, сокрытая от многих:"
        ]
        
        formatted = f"{emoji} <b>{random.choice(intros)}</b>\n\n"
        formatted += f"<i>«{text}»</i>\n\n"
        
        if quote_number is not None and total_quotes is not None:
            formatted += f"<code>Цитата #{quote_number + 1} из {total_quotes}</code>"
        
        return formatted
    
    @staticmethod
    def format_status(bot_name: str, start_time: datetime) -> str:
        """Форматировать статус бота"""
        uptime = datetime.now() - start_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        # Случайный статус
        statuses = [
            "✅ Активен и наблюдает",
            "👁️ Проклятый Взгляд открыт", 
            "⚡ Демоническая энергия стабильна",
            "🔮 Вещий и бодрствующий",
            "🎭 Баланс поддерживается"
        ]
        
        # Случайная мудрость
        wisdoms = [
            "«Равновесие — во всём»",
            "«Взгляд видит, уши слышат»",
            "«Даже в коде есть душа»",
            "«Баланс требует внимания»",
            "«Цифровой демон не дремлет»"
        ]
        
        return f"""
⚡ <b>СТАТУС {bot_name.upper()}</b>
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
<b>Состояние:</b> {random.choice(statuses)}
<b>Активен:</b> {days}д {hours}ч {minutes}м
<b>Время системы:</b> {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
<b>Лунная фаза:</b> {random.choice(['🌑 Новолуние', '🌒 Растущая', '🌕 Полнолуние', '🌘 Убывающая'])}
<b>Демонический заряд:</b> ▰▰▰▰▰ {random.randint(85, 100)}%

<i>{random.choice(wisdoms)}</i>

<code>Все системы функционируют нормально</code>
"""
    
    @staticmethod
    def format_help(commands: Dict[str, str]) -> str:
        """Форматировать помощь"""
        text = "📜 <b>СИЛЫ И КОМАНДЫ БАЛОРА</b>\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        text += "<i>«Выбери, что тебе нужно, смертный.»</i>\n\n"
        
        for cmd, desc in commands.items():
            text += f"• <code>/{cmd}</code> — {desc}\n"
        
        text += "\n<b>Секретные знания:</b>\n"
        text += "• Повторяй /lore — узнаешь всю историю\n"
        text += "• /quote показывает номер цитаты из коллекции\n"
        text += "• Проклятия имеют 5 уровней редкости\n"
        text += "• Бот реагирует на ключевые слова в сообщениях\n\n"
        
        text += "<i>Баланс — во всём. Даже в использовании команд.</i>\n\n"
        text += "<code>Балор слушает...</code>"
        
        return text

# ===================== ГЕНЕРАТОРЫ =====================
class CurseAnimator:
    """Анимация проклятий"""
    
    @staticmethod
    async def animate_roulette(message, edit_func):
        """Анимировать рулетку проклятий"""
        import asyncio
        
        symbols = ["🔮", "👁️", "⚡", "🔥", "💀", "👹", "😈", "🌀"]
        
        # Этап 1: Разгон
        await edit_func("🌀 *Собираю демоническую энергию...*")
        await asyncio.sleep(0.5)
        
        # Этап 2: Быстрое вращение
        for i in range(8):
            symbol = random.choice(symbols)
            speed = "⚡" * min(i + 1, 3)
            await edit_func(f"🎡 *Колесо крутится...* {speed}\n{symbol}")
            await asyncio.sleep(0.2)
        
        # Этап 3: Замедление
        for i in range(4):
            symbol = symbols[i % len(symbols)]
            await edit_func(f"🎡 *Замедляется...*\n{symbol}")
            await asyncio.sleep(0.3 + i * 0.1)
        
        # Финальная пауза
        await edit_func("🎰 *Судьба решает...*")
        await asyncio.sleep(0.5)

# ===================== СИСТЕМА ДОСТИЖЕНИЙ =====================
class AchievementSystem:
    """Система достижений"""
    
    ACHIEVEMENTS = {
        "curse_novice": {
            "name": "Новичок проклятий",
            "description": "Получить 5 проклятий",
            "emoji": "🔮",
            "condition": lambda stats: stats.get("curses_received", 0) >= 5
        },
        "curse_master": {
            "name": "Мастер проклятий", 
            "description": "Получить все уровни проклятий",
            "emoji": "👑",
            "condition": lambda stats: len(stats.get("tiers_received", set())) >= 5
        },
        "lore_seeker": {
            "name": "Искатель знаний",
            "description": "Узнать все части истории Балора",
            "emoji": "📚",
            "condition": lambda stats: stats.get("lore_parts_read", 0) >= 8
        },
        "quote_collector": {
            "name": "Коллекционер мудрости",
            "description": "Услышать 20 цитат",
            "emoji": "🗣️",
            "condition": lambda stats: stats.get("quotes_heard", 0) >= 20
        },
        "balor_friend": {
            "name": "Друг Балора",
            "description": "Общаться с ботом 7 дней подряд",
            "emoji": "🤝",
            "condition": lambda stats: stats.get("consecutive_days", 0) >= 7
        },
        "mythic_curse": {
            "name": "Проклятый судьбой",
            "description": "Получить МИФИЧЕСКОЕ проклятие",
            "emoji": "👁️",
            "condition": lambda stats: "MYTHIC" in stats.get("tiers_received", set())
        }
    }
    
    def __init__(self):
        self.user_stats = {}
    
    def update_stats(self, user_id: int, stat_type: str, value: Any = None):
        """Обновить статистику пользователя"""
        if user_id not in self.user_stats:
            self.user_stats[user_id] = {
                "curses_received": 0,
                "quotes_heard": 0,
                "lore_parts_read": 0,
                "tiers_received": set(),
                "achievements": set(),
                "last_active": datetime.now().date(),
                "consecutive_days": 1
            }
        
        stats = self.user_stats[user_id]
        
        if stat_type == "curse":
            stats["curses_received"] += 1
            if value and "tier" in value:
                stats["tiers_received"].add(value["tier"])
        
        elif stat_type == "quote":
            stats["quotes_heard"] += 1
        
        elif stat_type == "lore":
            stats["lore_parts_read"] += 1
        
        # Проверка последовательных дней
        today = datetime.now().date()
        if stats["last_active"] == today - timedelta(days=1):
            stats["consecutive_days"] += 1
        elif stats["last_active"] != today:
            stats["consecutive_days"] = 1
        
        stats["last_active"] = today
        
        return self.check_achievements(user_id)
    
    def check_achievements(self, user_id: int):
        """Проверить новые достижения"""
        if user_id not in self.user_stats:
            return []
        
        stats = self.user_stats[user_id]
        new_achievements = []
        
        for achievement_id, achievement in self.ACHIEVEMENTS.items():
            if (achievement_id not in stats["achievements"] and 
                achievement["condition"](stats)):
                
                stats["achievements"].add(achievement_id)
                new_achievements.append(achievement)
        
        return new_achievements
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Получить статистику пользователя"""
        return self.user_stats.get(user_id, {})

# ===================== УТИЛИТЫ =====================
def generate_id(text: str, length: int = 8) -> str:
    """Сгенерировать ID из текста"""
    return hashlib.md5(text.encode()).hexdigest()[:length].upper()

def get_random_response() -> str:
    """Получить случайный ответ на обычное сообщение"""
    responses = [
        "Интересно... продолжай.",
        "Мой Взгляд видит смысл в твоих словах.",
        "Записываю в демонические скрижали.",
        "И что мне с этой информацией делать?",
        "Ты говоришь, а я слушаю... вроде бы.",
        "Проклятый Взгляд наблюдает. Продолжай.",
        "В твоих словах есть... потенциал.",
        "Хм. Интересная точка зрения.",
        "Даже демоны учатся новому. Говори дальше.",
        "Запомню это. Возможно."
    ]
    
    return random.choice(responses)

def get_keyword_response(text: str) -> str:
    """Получить ответ на ключевые слова"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['привет', 'здравствуй', 'hello', 'hi']):
        return "Приветствую. Чего желаешь?"
    
    elif any(word in text_lower for word in ['спасибо', 'благодарю', 'thanks']):
        return "Не благодари. Просто поддерживай баланс."
    
    elif any(word in text_lower for word in ['пока', 'прощай', 'до свидания', 'bye']):
        return "Прощай. Возвращайся, когда понадоблюсь."
    
    elif any(word in text_lower for word in ['балор', 'бесобой', 'проклятый взгляд']):
        return "Ты произнёс моё имя. Будь осторожен в желаниях."
    
    elif '?' in text:
        return random.choice([
            "Интересный вопрос. Спроси ещё раз после полуночи.",
            "Проклятый Взгляд видит ответ, но он тебе не понравится.",
            "У всего есть цена. Ты готов заплатить за ответ?",
            "Спроси у звёзд. Они болтливее меня."
        ])
    
    return None
