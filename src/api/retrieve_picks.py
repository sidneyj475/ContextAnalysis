import requests
import time
from tenacity import retry, stop_after_attempt, wait_fixed
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent 
ENV_PATH = BASE_DIR / "config" / ".env"

load_dotenv(dotenv_path=ENV_PATH)

AUTH_KEY = os.getenv("MON_AUTH_KEY")
USER_ID = os.getenv("MON_USER_ID")
REFERER= os.getenv("MON_REFERER")
ORIGIN= os.getenv("MON_ORIGIN")
PICKS_URL= os.getenv("MON_PICKS_URL")

time.sleep(2)  # 2-second delay between requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Accept": "application/json",
    "authorization": AUTH_KEY,
    "Referer": REFERER,
    "Origin": ORIGIN
}

@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def fetch_player_picks(league, market, sportsbooks):
    """
    Fetch player props from machine learning model.
    """
    url = PICKS_URL
    params = {
        "user_id": USER_ID,  # Your user ID
        "league": league,
        "market": market,
        "sportsbooks": sportsbooks
    }

    response = requests.post(
        url,
        headers=HEADERS,
        params=params
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def quick_print(picks):
    for pick in picks:
        print(f"{pick['selection']} | {pick['formatted_market']} {pick['line']}")
        print(f"O/U: {pick['selection_line']} | Prob: {pick['simulated_prob']*100:.1f}%")
        print("─" * 40)

#usage
picks = fetch_player_picks(league="NBA", market="All", sportsbooks="bovada")
quick_print(picks)