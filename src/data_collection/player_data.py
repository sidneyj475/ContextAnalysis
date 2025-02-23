from basketball_reference_scraper.players import get_game_logs

df = get_game_logs("Amen Thompson", 2025, playoffs=False)
print(df)