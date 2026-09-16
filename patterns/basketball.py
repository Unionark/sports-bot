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
