import asyncio
import importlib
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from patterns.models import AlertSignal

# ── Все паттерны на едином формате (analyze → AlertSignal) ──
enabled_patterns = ['basketball', 'tennis', 'hockey', 'volleyball', 'yellow_cards']

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
    # Теннис
    test_tennis = {
        "match_id": "test_tennis",
        "player1": "Кори Гауфф",
        "player2": "Арина Соболенко",
        "gender": "women",
        "set_results": [4, 6],
        "p1_double_faults_set1": 2,
        "p2_double_faults_set1": 1,
    }
    # Хоккей
    test_hockey = {
        "match_id": "test_hockey",
        "home": "ЦСКА",
        "away": "Динамо",
        "period_1_home_score": 0,
        "period_1_away_score": 2,
        "odds": 5.0,
    }
    # Волейбол
    test_volleyball = {
        "match_id": "test_volleyball",
        "sport": "volleyball",
        "gender": "women",
        "match_type": "league",
        "home": "Динамо М",
        "away": "Локомотив",
        "sets": {"set_1_total_points": 48},
    }
    # Футбол (жёлтые карточки)
    test_football = {
        "match_id": "test_football",
        "home": "Зенит",
        "away": "Спартак",
        "minute": 75,
        "score_diff": 1,
        "yellow_cards_2nd_half": 2,
        "ppda_1st_half": 7,
    }

    results = []
    for label, match in [("теннис", test_tennis), ("хоккей", test_hockey),
                         ("волейбол", test_volleyball), ("футбол", test_football)]:
        signals = process_match(match)
        if signals:
            for s in signals:
                results.append(f"⚠️ [{label}] {s.sport}: {s.message}")
        else:
            results.append(f"[{label}] Сигналов нет.")

    await message.answer("\n\n".join(results))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
