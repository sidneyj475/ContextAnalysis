from team_mappings import TEAM_ABBREVIATIONS

def clean_opponent(raw_opponent: str) -> str:
    """Clean opponent names from ESPN data"""
    cleaned = raw_opponent.replace('@', '').replace('vs', '').strip()
    return TEAM_ABBREVIATIONS.get(cleaned.upper(), cleaned)

def safe_float(value: str) -> float:
    """Safely convert string values to floats"""
    try:
        return float(value.split('-')[0])  # Take first value if range
    except:
        return 0.0