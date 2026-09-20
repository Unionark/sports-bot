from dataclasses import dataclass

@dataclass
class AlertSignal:
    match_id: str
    sport: str
    event_type: str
    message: str
    priority: int
