from .models import AlertSignal

volleyball_patterns = {
    "patternstar_high_first_set_total": {
        "sport": "volleyball",
        "conditions": {
            "gender": "women",
            "match_type_exclude": "friendly",
            "set_1_total_min": 45.5
        },
        "prediction": "high_set_1",
        "message": "Матч {home} — {away}. Женский волейбол, не товарищеский. Тотал 1‑й партии: {set_1_total} (>45.5). Прогноз: высокая результативность в матче."
    }
}

def analyze(match_data):
    signals = []
    for pattern_name, pattern in volleyball_patterns.items():
        conds = pattern["conditions"]

        sport = match_data.get("sport")
        gender = match_data.get("gender")
        match_type = match_data.get("match_type")
        sets = match_data.get("sets", {})
        set_1_total = sets.get("set_1_total_points")
        home = match_data.get("home")
        away = match_data.get("away")

        if sport != "volleyball":
            continue
        if gender != conds["gender"]:
            continue
        if match_type == conds["match_type_exclude"]:
            continue
        if set_1_total is None or set_1_total <= conds["set_1_total_min"]:
            continue

        msg = pattern["message"].format(
            home=home,
            away=away,
            set_1_total=set_1_total
        )

        signals.append(AlertSignal(
            match_id=match_data.get("match_id", f"{home}_vs_{away}"),
            sport="volleyball",
            event_type=pattern_name,
            message=msg,
            priority=2,
        ))

    return signals
