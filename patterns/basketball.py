from .models import AlertSignal

basketball_patterns = {
    "favorite_wins_q1_underdog_x2_q2": {
        "sport": "basketball",
        "conditions": {
            "favorite_odds_min": 1.1,
            "favorite_odds_max": 1.5,
            "favorite_won_q1": True
        },
        "prediction": "X2",
        "prediction_target": "underdog",
        "prediction_quarter": 2,
        "message": "Фаворит выиграл первую четверть. Прогноз: X2 на аутсайдера во второй четверти."
    },
    "same_parity_q1_q2_opposite_q3": {
        "sport": "basketball",
        "conditions": {
            "q1_q2_same_parity": True
        },
        "prediction": "opposite_parity",
        "prediction_quarter": 3,
        "message": "Первая и вторая четверть закончились с одинаковой чётностью/нечётностью. Прогноз: 3-я четверть — {parity}."
    }
}


def analyze(match_data):
    signals = []
    for pattern_name, pattern in basketball_patterns.items():
        # TODO: здесь будет проверка условий паттерна по match_data
        # Пока — заглушка: если есть счёт, генерируем сигнал
        if match_data.score:
            signals.append(AlertSignal(
                match_id=match_data.match_id,
                sport=match_data.sport,
                event_type=pattern_name,
                message=pattern["message"],
                priority=2
            ))
    return signals
    
