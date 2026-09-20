from .models import AlertSignal

yellow_cards_patterns = {
    "late_escalation": {
        "conditions": {"minute_min": 70, "yellow_cards_2nd_half_min": 2},
        "message": "Эскалация дисциплины: матч {minute} мин, {yellow_cards_2nd_half} ЖК во 2-м тайме. Риск красных и тоталов."
    },
    "chasing_the_score": {
        "conditions": {"score_diff_not_zero": True, "yellow_cards_2nd_half_min": 1},
        "message": "Фрустрация погони: команда проигрывает и уже имеет ЖК. Риск серии фолов."
    },
    "high_press_fatigue": {
        "conditions": {"minute_min": 60, "ppda_1st_half_max": 10},
        "message": "Усталость прессинга: высокий прессинг в 1-м тайме + {minute} мин. Риск тактических фолов."
    },
}


def analyze(match_data):
    signals = []
    minute = match_data.get("minute", 0)
    score_diff = match_data.get("score_diff", 0)
    yc_2nd = match_data.get("yellow_cards_2nd_half", 0)
    ppda_1st = match_data.get("ppda_1st_half", 20)
    home = match_data.get("home", "?")
    away = match_data.get("away", "?")

    # late_escalation
    if minute > 70 and yc_2nd >= 2:
        signals.append(AlertSignal(
            match_id=match_data.get("match_id", f"{home}_vs_{away}"),
            sport="football",
            event_type="late_escalation",
            message=yellow_cards_patterns["late_escalation"]["message"].format(
                minute=minute, yellow_cards_2nd_half=yc_2nd
            ),
            priority=2,
        ))

    # chasing_the_score
    if score_diff != 0 and yc_2nd >= 1:
        signals.append(AlertSignal(
            match_id=match_data.get("match_id", f"{home}_vs_{away}"),
            sport="football",
            event_type="chasing_the_score",
            message=yellow_cards_patterns["chasing_the_score"]["message"],
            priority=2,
        ))

    # high_press_fatigue
    if minute >= 60 and ppda_1st < 10:
        signals.append(AlertSignal(
            match_id=match_data.get("match_id", f"{home}_vs_{away}"),
            sport="football",
            event_type="high_press_fatigue",
            message=yellow_cards_patterns["high_press_fatigue"]["message"].format(minute=minute),
            priority=2,
        ))

    return signals
