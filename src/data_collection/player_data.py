import requests
from bs4 import BeautifulSoup
from typing import Dict, List
from utils.data_cleaner import clean_opponent, safe_float
import os
from dotenv import load_dotenv
from pathlib import Path

#path to env file
BASE_DIR = Path(__file__).resolve().parent.parent.parent 
ENV_PATH = BASE_DIR / "config" / ".env"

load_dotenv(dotenv_path=ENV_PATH)

#set key pairs
SEARCH_URL = os.getenv("E_SEARCH_URL")
LOG_URL = os.getenv("E_LOG_URL")

class PlayerData:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    def get_game_logs(self, player_name: str) -> List[Dict]:
        #Get cleaned game logs for a player
        player_id = self._get_player_id(player_name)
        if not player_id:
            return []
            
        raw_logs = self._fetch_raw_game_logs(player_id)
        return self._clean_game_logs(raw_logs)

    def _get_player_id(self, player_name: str) -> str:
        #Get player ID
        search_url = SEARCH_URL
        params = {
            "query": player_name,
            "limit": 5,
            "type": "player",
            "sport": "basketball"
        }
        
        try:
            #print(f"\nSearching for {player_name}...")
            response = requests.get(search_url, params=params)
            data = response.json()
            #print(f"Debug - Search response: {data}")  # Print response data
            
            if 'items' in data and len(data['items']) > 0:
                for item in data['items']:
                    if item['displayName'].lower() == player_name.lower():
                        player_id = item['id']
                        #print(f"Debug - Found player ID: {player_id}")
                        return {"success": True, "id": player_id}
                player_id = data['items'][0]['id']
                #print(f"Debug - Using first result ID: {player_id}")
                return {"success": True, "id": player_id}
            return {"success": False, "error": "Player not found"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
        
    def _fetch_raw_game_logs(self, player_id: str) -> List[Dict]:
        # Get game log data
        url = LOG_URL
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            return self._parse_gamelog_table(soup)
        except:
            return []

    def _parse_gamelog_table(self, soup) -> List[Dict]:
        #Parse game log table
        games = []
        tables = soup.find_all('table', class_='Table')
        
        for table in tables:
            for row in table.find_all('tr')[1:]:  # Skip header
                cells = [td.get_text(strip=True) for td in row.find_all('td')]
                if len(cells) < 15:
                    continue
                    
                games.append({
                    'date': cells[0],
                    'opponent': clean_opponent(cells[1]),
                    'points': safe_float(cells[5]),
                    'rebounds': safe_float(cells[7]),
                    'assists': safe_float(cells[8]),
                    'threes_made': safe_float(cells[4])
                })
                
        return games