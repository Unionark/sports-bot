from .models import AlertSignal

hockey_patterns = {
    "team_lost_02_first_period_scores_in_second": {
        "sport": "hockey",
        "conditions": {
            "period_1_score_diff": -2,
            "period_1_score_against": 2,
            "odds_max": 7.0
        },
        "prediction": "scores_in_second",
        "prediction_target": "losing_team",
        "prediction_period": 2,
        "message": "Матч {home} — {away}. Команда {losing_team} проиграла 1-й период со счётом 0:2. Прогноз: команда {losing_team} забьёт во 2-м периоде."
    }
}


def analyze(match_data):
    signals = []
    for pattern_name, pattern in hockey_patterns.items():
        conds = pattern["conditions"]

        p1_home = match_data.get("period_1_home_score")
        p1_away = match_data.get("period_1_away_score")
        home = match_data.get("home")
        away = match_data.get("away")
        odds = match_data.get("odds")

        if p1_home is None or p1_away is None:
            continue

        if p1_home < p1_away:
            losing_team = home
            score_diff = p1_home - p1_away
        else:
            losing_team = away
            score_diff = p1_away - p1_home

        if score_diff != conds["period_1_score_diff"]:
            continue

        if odds and odds > conds["odds_max"]:
            continue

        msg = pattern["message"].format(
            home=home,
            away=away,
            losing_team=losing_team
        )

        signals.append(AlertSignal(
            match_id=match_data.get("match_id", f"{home}_vs_{away}"),
            sport="hockey",
            event_type=pattern_name,
            message=msg,
            priority=2,
        ))

    return signals
