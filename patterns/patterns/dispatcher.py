from typing import List
from .models import AlertSignal
from .basketball import analyze as analyze_basketball
from .hockey import analyze as analyze_hockey
from .volleyball_pattern import analyze as analyze_volleyball

PATTERNS = {
    "basketball": analyze_basketball,
    "hockey": analyze_hockey,
    "volleyball": analyze_volleyball,
}

def dispatch(match_data) -> List[AlertSignal]:
    handler = PATTERNS.get(match_data.sport)
    if not handler:
        return []
    return handler(match_data)
  
