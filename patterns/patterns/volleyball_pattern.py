from patterns.models import AlertSignal

def analyze(match_data):
    signals = []
    
    # Паттерн: тотал первой партии > 45 очков → сигнал на тотал второй партии
    sets = match_data.get("sets", {})
    set_1_total = sets.get("set_1_total_points", 0)
    if set_1_total > 45:
        signals.append(AlertSignal(
            sport="volleyball",
            message="Тотал 1-й партии высокий ({} очков) — вероятен тотал 2-й партии > 46".format(set_1_total),
            value=set_1_total,
            pattern="high_set1_total"
        ))
    
    # Паттерн: если в 1-й партии разница ≤ 2 очка — возможен упорный матч
    if 1 <= set_1_total <= 50 and match_data.get("gender") == "women":
        signals.append(AlertSignal(
            sport="volleyball",
            message="Упорная 1-я партия у женщин — возможен тотал матча > 135",
            value=set_1_total,
            pattern="close_set1_women"
        ))

    return signals
