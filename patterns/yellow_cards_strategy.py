"""
patterns/yellow_cards/yellow_cards_strategy.py

Стратегия анализа жёлтых карточек во втором тайме.
Реализует логику: усталость прессинга, фрустрация при отставании, эскалация в концовке.
"""

from typing import Dict, Tuple, Optional

def trigger_late_escalation(stats: Dict) -> Tuple[bool, Optional[str]]:
    """
    Паттерн: «Эскалация в концовке».
    Если матч идёт больше 70 минут и количество ЖК во втором тайме >= 2,
    считаем, что команда входит в фазу «дисциплинарного коллапса».
    """
    minute = stats.get("minute", 0)
    yellow_cards_2nd_half = stats.get("yellow_cards_2nd_half", 0)
    
    if minute > 70 and yellow_cards_2nd_half >= 2:
        return True, "Эскалация дисциплины: матч > 70 мин, 2+ ЖК во 2-м тайме. Риск красных и тоталов."
    return False, None

def trigger_chasing_the_score(stats: Dict) -> Tuple[bool, Optional[str]]:
    """
    Паттерн: «Фрустрация погони».
    Если команда проигрывает и у неё уже есть хотя бы 1 ЖК во втором тайме,
    вероятность следующей карточки резко возрастает из-за отчаянных подкатов.
    """
    score_diff = stats.get("score_diff", 0)  # Положительное число, если хозяева проигрывают
    yellow_cards_2nd_half = stats.get("yellow_cards_2nd_half", 0)
    
    # score_diff > 0 означает, что хозяева проигрывают. 
    # Если мы проверяем гостевую команду, логика инвертируется. 
    # Здесь упрощаем: если кто-то проигрывает и уже фолит.
    
    is_chasing = score_diff != 0  # Кто-то проигрывает
    
    if is_chasing and yellow_cards_2nd_half >= 1:
        return True, "Фрустрация погони: команда проигрывает и уже имеет ЖК. Риск серии фолов."
    return False, None

def trigger_high_press_fatigue(stats: Dict) -> Tuple[bool, Optional[str]]:
    """
    Паттерн: «Усталость прессинга».
    Если в первом тайме команда много прессинговала (условно PPDA < 10) 
    и сейчас идёт 60+ минута, риск реактивных фолов высок.
    """
    minute = stats.get("minute", 0)
    ppda_1st_half = stats.get("ppda_1st_half", 20)  # Чем меньше число, тем выше прессинг
    
    if minute >= 60 and ppda_1st_half < 10:
        return True, "Усталость прессинга: высокий прессинг в 1-м тайме + 60+ минута. Риск тактических фолов."
    return False, None

def evaluate_yellow_card_pattern(match_stats: Dict) -> Tuple[bool, str]:
    """
    Главная функция стратегии.
    Проверяет все триггеры. Если сработал хотя бы один — возвращает True и описание.
    
    Ожидаемый формат match_stats:
    {
        "minute": 65,
        "score_diff": 1,  # Разница голов (хозяева - гости). 1 = хозяева проигрывают 0:1
        "yellow_cards_2nd_half": 1,
        "ppda_1st_half": 8
    }
    """
    triggers = [
        trigger_late_escalation,
        trigger_chasing_the_score,
        trigger_high_press_fatigue
    ]
    
    for trigger_func in triggers:
        is_matched, message = trigger_func(match_stats)
        if is_matched:
            return True, message
            
    return False, "Паттерн по жёлтым карточкам не сработал."

# Пример использования (для локальной проверки перед вставкой в main.py)
if __name__ == "__main__":
    # Тестовый матч: 75 минута, хозяева проигрывают 0:1, 2 ЖК во втором тайме, прессинг был высоким
    test_match = {
        "minute": 75,
        "score_diff": 1,
        "yellow_cards_2nd_half": 2,
        "ppda_1st_half": 7
    }
    
    matched, reason = evaluate_yellow_card_pattern(test_match)
    print(f"Сработало: {matched}. Причина: {reason}")

