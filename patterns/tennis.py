from .models import AlertSignal

# Топ-25 мужчин: рост двойных ошибок после проигранного сета (в процентах)
MEN_TOP_25 = {
    "Денис Шаповалов": 75,
    "Александр Бублик": 72,
    "Майкл Ммо": 68,
    "Джейкоб Фирнли": 65,
    "Шинтаро Мочизуки": 62,
    "Эльмер Мёллер": 60,
    "Николоз Басилашвили": 58,
    "Даниил Медведев": 55,
    "Густаво Хайде": 52,
    "Новак Джокович": 50,
    "Хайме Фария": 48,
    "Далибор Сврчина": 45,
    "Нишеш Басаваредди": 43,
    "Ботик ван де Зандшульп": 42,
    "Мартин Ландалусэ": 40,
    "Маттео Арнальди": 38,
    "Зизу Бергс": 36,
    "Григор Димитров": 34,
    "Лёнер Тьен": 32,
    "Феликс Оже-Альяссим": 30,
    "Карлос Алькарас": 28,
    "Якуб Меншик": 25,
    "Райлли Опелка": 22,
    "Александр Зверев": 18,
    "Суну Квон": 15,
}

# Топ-25 женщин: рост двойных ошибок после проигранного сета (в процентах)
WOMEN_TOP_25 = {
    "Кори Гауфф": 95,
    "Оксана Селехметева": 90,
    "Алисия Паркс": 85,
    "Паула Бадоса": 82,
    "Маркета Вондоушова": 80,
    "Айла Томлянович": 75,
    "Елена Остапенко": 72,
    "Дарья Касаткина": 70,
    "Марта Костюк": 65,
    "Джессика Бузас Манейро": 62,
    "Даяна Ястремская": 58,
    "Линда Носкова": 55,
    "Екатерина Александрова": 52,
    "Аманда Анисимова": 48,
    "Арина Соболенко": 45,
    "Лейла Фернандес": 42,
    "Анастасия Потапова": 40,
    "Ева Лис": 38,
    "София Кенин": 36,
    "Эмма Наварро": 34,
    "Элисе Мертенс": 32,
    "Барбора Крейчикова": 30,
    "Каролина Мухова": 28,
    "Ига Швёнтек": 25,
    "Чжэн Циньвэнь": 22,
}


def get_player_boost(player_name, gender):
    if gender == "men":
        return MEN_TOP_25.get(player_name)
    elif gender == "women":
        return WOMEN_TOP_25.get(player_name)
    return None


def analyze(match_data):
    """
    Анализирует матч на срабатывание паттерна «рост двойных ошибок после проигранного сета».
    
    Вход: match_data — словарь с данными матча.
    Пример:
    {
      "player1": "Кори Гауфф",
      "player2": "Арина Соболенко",
      "gender": "women",
      "set_results": [4, 6],
      "p1_double_faults_set1": 2,
      "p2_double_faults_set1": 1,
      "total_points_set1": 20
    }
    
    Выход: список объектов AlertSignal (может быть пустым).
    """
    signals = []

    p1 = match_data.get("player1")
    p2 = match_data.get("player2")
    gender = match_data.get("gender")
    set_results = match_data.get("set_results")

    if not all([p1, p2, gender, set_results]) or len(set_results) < 2:
        return signals

    s1_p1 = set_results
    s1_p2 = set_results

    # Кто проиграл первый сет
    loser = p1 if s1_p1 < s1_p2 else p2
    # winner = p1 if s1_p1 > s1_p2 else p2  # winner не используется в текущей логике

    boost_percent = get_player_boost(loser, gender)
    if boost_percent is None:
        return signals  # игрок не в топ-25 — паттерн не срабатывает

    # Сколько двойных было в 1-м сете у проигравшего
    loser_df_set1 = None
    if loser == p1:
        loser_df_set1 = match_data.get("p1_double_faults_set1")
    else:
        loser_df_set1 = match_data.get("p2_double_faults_set1")

    if loser_df_set1 is None:
        return signals

    # Прогноз: ожидаемое количество двойных во 2-м сете с учётом роста на boost_percent%
    expected_df_set2 = loser_df_set1 * (1 + boost_percent / 100.0)

    forecast_text = (
        f"{loser} проиграл первый сет {s1_p1}-{s1_p2}. "
        f"Прогноз на 2-й сет: количество двойных ошибок ожидается больше {expected_df_set2:.1f} "
        f"(рост на {boost_percent}% по статистике топ-игроков)."
    )

    signals.append(
        AlertSignal(
            match_id=match_data.get("match_id", f"{p1}_vs_{p2}"),
            sport="tennis",
            event_type="double_faults_after_lost_set",
            message=forecast_text,
            priority=2,
            extra={
                "loser": loser,
                "boost_percent": boost_percent,
                "expected_df_set2": expected_df_set2,
                "set_results": set_results,
            },
        )
    )

    return signals
