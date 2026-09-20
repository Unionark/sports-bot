from dataclasses import dataclass
from typing import Any, Dict, List, Optional

@dataclass
class MatchData:
    match_id: str
    sport: str
    status: str
    home_team: str
    away_team: str
    score: Optional[Dict[str, int]]
    events: List[Dict[str, Any]]
    raw: Dict[str, Any]


class FlashScoreAdapter:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_match_data(self, match_id: str) -> MatchData:
        # TODO: здесь будет реальный запрос к FlashScore
        # Для MVP — заглушка с тестовыми данными
        return MatchData(
            match_id=match_id,
            sport="football",
            status="live",
            home_team="Team A",
            away_team="Team B",
            score={"home": 1, "away": 0},
            events=[
                {"type": "yellow_card", "player": "Player X", "time": 25}
            ],
            raw={}
                 )
      
