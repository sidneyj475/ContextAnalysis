# Updated player_data.py
from basketball_reference_scraper.players import get_game_logs
from api.retrieve_picks import fetch_player_picks

def process_picks_to_names(picks):
    #Extract player names from picks data
    player_names = []
    for pick in picks:
        # Split on first numerical value to remove odds
        parts = pick['selection'].split()
        name_parts = []
        for part in parts:
            if any(char.isdigit() for char in part):
                break
            name_parts.append(part)
        player_names.append(' '.join(name_parts))
    return player_names

# Get current picks
picks = fetch_player_picks(league="NBA", market="player_threes", sportsbooks="bovada", bet_name="Amen Thompson 8.5")

if picks:
    # Extract and clean player names from picks
    players = process_picks_to_names(picks)
    
    # Get game logs for each player
    for player in players:
        print(f"\nFetching game logs for {player}...")
        try:
            df = get_game_logs(player, 2025, playoffs=False)
            print(df.tail(5))  # Show first 5 games
        except Exception as e:
            print(f"Error getting logs for {player}: {str(e)}")
else:
    print("No picks retrieved")


