# patterns/volleyball_pattern.py

def check_volleyball_pattern(match: dict) -> bool:
    """
    Проверяет срабатывание паттерна «Patternstar»:
    - вид спорта: волейбол
    - пол: женщины
    - тип матча: не товарищеский
    - тотал 1‑й партии > 45.5
    
    :param match: словарь с данными матча
    :return: True, если паттерн сработал, иначе False
    """
    if match.get("sport") != "volleyball":
        return False
    if match.get("gender") != "women":
        return False
    if match.get("match_type") == "friendly":
        return False

    sets = match.get("sets", {})
    set_1_total = sets.get("set_1_total_points")

    if set_1_total is None:
        return False

    return set_1_total > 45.5
  
