from patterns.models import AlertSignal

def analyze(match_data):
    signals = []
    
    # Паттерн: во 2-м тайме ≥2 жёлтых — сигнал на тотал ЖК ≥4 в матче
    yellow_2nd = match_data.get("yellow_cards_2nd_half", 0)
    if yellow_2nd >= 2:
        signals.append(AlertSignal(
            sport="football",
            message="Во 2-м тайме уже {} жёлтых — вероятен тотал ЖК ≥4 за матч".format(yellow_2nd),
            value=yellow_2nd,
            pattern="high_yellow_2nd"
        ))
    
    # Паттерн: разница в счёте = 1 и минута ≥75 — возможен рост ЖК из‑за напряжения
    minute = match_data.get("minute", 0)
    score_diff = match_data.get("score_diff", 0)
    if minute >= 75 and score_diff == 1:
        signals.append(AlertSignal(
            sport="football",
            message="75+ минута, разница в 1 мяч — риск роста жёлтых карточек",
            value=minute,
            pattern="late_close_game_yellow"
          
