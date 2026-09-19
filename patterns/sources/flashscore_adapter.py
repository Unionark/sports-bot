"""
sources/flashscore_adapter.py
Универсальный адаптер FlashScore для всех стратегий и видов спорта.
Футбол, теннис, волейбол, баскетбол — один интерфейс.
"""
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
}

BASE_URL = "https://www.flashscore.com"

def get_live_matches(sport="football"):
    """
    Возвращает список ID live-матчей по виду спорта.
    sport: football, tennis, volleyball, basketball
    """
    url = f"{BASE_URL}/{sport}/"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return _parse_match_ids(response.text)
    except Exception as e:
        print(f"Ошибка запроса ({sport}): {e}")
        return []

def _parse_match_ids(html):
    """Извлекает ID матчей из HTML."""
    if not html:
        return []
    soup = BeautifulSoup(html, 'lxml')
    ids = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '/match/' in href and len(href.split('/')) >= 3:
            mid = href.split('/')[2]
            if mid not in ids:
                ids.append(mid)
    return ids

def get_match_stats(match_id, sport="football"):
    """
    Возвращает статистику матча в едином формате для всех стратегий.
    Сейчас — заглушка с тестовыми данными.
    Реальный парсинг подключим, когда найдём JSON-эндпоинт FlashScore.
    """
    base = {
        "match_id": match_id,
        "sport": sport,
        "minute": 68,
    }

    if sport == "football":
        base.update({
            "score_diff": 1,
            "yellow_cards_2nd_half": 2,
            "ppda_1st_half": 9,
        })
    elif sport == "tennis":
        base.update({
            "set": 2,
            "double_faults": 3,
            "server": "player_1",
        })
    elif sport == "volleyball":
        base.update({
            "set": 3,
            "score_diff": 2,
        })
    elif sport == "basketball":
        base.update({
            "quarter": 3,
            "score_diff": 5,
        })
    else:
        base.update({"score_diff": 0})

    return base

def get_all_live_stats(sport="football"):
    """
    Главный метод: берёт все live-матчи и отдаёт статистику по каждому.
    Вызывается из main.py для любого вида спорта.
    """
    match_ids = get_live_matches(sport)
    results = []
    for mid in match_ids:
        stats = get_match_stats(mid, sport)
        results.append(stats)
    return results
