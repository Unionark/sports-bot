import asyncio
import importlib
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from patterns.models import AlertSignal

# ── Паттерны на едином формате (analyze → AlertSignal) ──
enabled_patterns = ['basketball', 'tennis']

# ── Паттерны, ещё не переведённые (оставлены как есть) ──
from patterns.volleyball_pattern import check_volleyball_pattern
from patterns.yellow_cards.yellow_cards_strategy import evaluate_yellow_card_pattern
from patterns.hockey import hockey_patterns

# ── Flashscore (заглушка — заполни ключ/функцию получения данных) ──
async def fetch_flashscore_match(match_id):
    # TODO: реализовать запрос к Flashscore API
    # Должен возвращать словарь match_data для process_match
    pass

API_TOKEN = '8595642966:AAG4eVdxKpeISbuQIJzIG0EfweFeNB-V5Xg'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


def load_patterns():
    analyzers = []
    for module_name in enabled_patterns:
        try:
            module = importlib.import_module(f'patterns.{module_name}')
            if hasattr(module, 'analyze'):
                analyzers.append(module.analyze)
        except ImportError as e:
            print(f"[ERROR] Не удалось загрузить {module_name}: {e}")
    return analyzers


all_analyzers = load_patterns()


def process_match(match_data):
    all_signals = []
    for analyze_func in all_analyzers:
        try:
            signals = analyze_func(match_data)
            if signals:
                all_signals.extend(signals)
        except Exception as e:
            print(f"Ошибка: {e}")
    return all_signals


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я спортивный бот. Чем могу помочь?")


@dp.message(Command("test"))
async def cmd_test(message: types.Message):
    test_match = {
        "match_id": "test_001",
        "player1": "Кори Гауфф",
        "player2": "Арина Соболенко",
        "gender": "women",
        "set_results": [4, 6],
        "p1_double_faults_set1": 2,
        "p2_double_faults_set1": 1,
    }
    signals = process_match(test_match)
    if signals:
        for s in signals:
            await message.answer(f"⚠️ {s.sport}: {s.message}")
    else:
        await message.answer("Сигналов нет.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
