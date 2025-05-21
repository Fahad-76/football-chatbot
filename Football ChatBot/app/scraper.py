# scraper.py
# Scrapes 2024–25 Premier League player stats team-by-team from FBref

import requests
import pandas as pd
import time
from bs4 import BeautifulSoup

# ============================
# Function: Extract player data from a team page
# ============================
def get_player_info(soup, team_name):
    # Find the main stats table for players on the team page
    table = soup.find("table", {"id": "stats_standard_combined"})
    players = []

    # Handle case where table isn't found
    if not table:
        print(f"⚠️ No player stats table found for {team_name}")
        return players

    # Loop through each player row in the table
    for row in table.find("tbody").find_all("tr"):
        cols = row.find_all("td")
        if len(cols) > 0:
            # Extract key fields for each player
            player = row.find('th', {'data-stat': 'player'}).text.strip()
            position = row.find('td', {'data-stat': 'position'}).text.strip()
            age = row.find('td', {'data-stat': 'age'}).text.strip()
            goals = row.find('td', {'data-stat': 'goals'}).text.strip()
            assists = row.find('td', {'data-stat': 'assists'}).text.strip()

            # Convert to integers (default to 0 if missing or invalid)
            goals = int(goals) if goals.isdigit() else 0
            assists = int(assists) if assists.isdigit() else 0
            ga = goals + assists

            # Store player data
            players.append({
                "team": team_name,
                "player": player,
                "position": position,
                "age": age,
                "goals": goals,
                "assists": assists,
                "ga": ga
            })

    return players

#scrapes a single url if any was missed
def scrape_single_team(url):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd

    from app.scraper import get_player_info  # if defined separately

    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "html.parser")

        team_name = soup.find("h1").text.strip().replace(" Stats", "")
        players = get_player_info(soup, team_name)
        df_new = pd.DataFrame(players)

        # Load existing file
        df_old = pd.read_csv("data/premier_league_2024_25.csv")

        # Combine and drop duplicate rows based on player+team
        df_combined = pd.concat([df_old, df_new])
        df_combined.drop_duplicates(subset=["player", "team"], keep="last", inplace=True)

        # Save updated data
        df_combined.to_csv("data/premier_league_2024_25.csv", index=False)
        print(f"✅ Appended data for {team_name}")

    except Exception as e:
        print(f"❌ Failed to scrape {url}: {e}")

# ============================
# Function: Scrape all team pages
# ============================
def scrape_all_teams():
    # Hardcoded list of URLs for each Premier League team in 2024–25
    team_urls = [
        "https://fbref.com/en/squads/18bb7c10/2024-2025/all_comps/Arsenal-Stats-All-Competitions",
        "https://fbref.com/en/squads/7c21e445/2024-2025/all_comps/Aston-Villa-Stats-All-Competitions",
        "https://fbref.com/en/squads/ccf3bfcb/2024-2025/all_comps/Bournemouth-Stats-All-Competitions",
        "https://fbref.com/en/squads/d07537b9/2024-2025/all_comps/Brentford-Stats-All-Competitions",
        "https://fbref.com/en/squads/943e8050/2024-2025/all_comps/Brighton-and-Hove-Albion-Stats-All-Competitions",
        "https://fbref.com/en/squads/cd051869/2024-2025/all_comps/Burnley-Stats-All-Competitions",
        "https://fbref.com/en/squads/47c64c55/2024-2025/all_comps/Chelsea-Stats-All-Competitions",
        "https://fbref.com/en/squads/d3fd31cc/2024-2025/all_comps/Crystal-Palace-Stats-All-Competitions",
        "https://fbref.com/en/squads/1df6b87e/2024-2025/all_comps/Everton-Stats-All-Competitions",
        "https://fbref.com/en/squads/8602292d/2024-2025/all_comps/Fulham-Stats-All-Competitions",
        "https://fbref.com/en/squads/4ba7cbea/2024-2025/all_comps/Ipswich-Town-Stats-All-Competitions",
        "https://fbref.com/en/squads/822bd0ba/2024-2025/all_comps/Liverpool-Stats-All-Competitions",
        "https://fbref.com/en/squads/b8fd03ef/2024-2025/all_comps/Manchester-City-Stats-All-Competitions",
        "https://fbref.com/en/squads/19538871/2024-2025/all_comps/Manchester-United-Stats-All-Competitions",
        "https://fbref.com/en/squads/e4a775cb/2024-2025/all_comps/Newcastle-United-Stats-All-Competitions",
        "https://fbref.com/en/squads/fd962109/2024-2025/all_comps/Nottingham-Forest-Stats-All-Competitions",
        "https://fbref.com/en/squads/33c895d4/2024-2025/all_comps/Sheffield-United-Stats-All-Competitions",
        "https://fbref.com/en/squads/361ca564/2024-2025/all_comps/Tottenham-Hotspur-Stats-All-Competitions",
        "https://fbref.com/en/squads/1c781004/2024-2025/all_comps/West-Ham-United-Stats-All-Competitions",
        "https://fbref.com/en/squads/1df6b87e/2024-2025/all_comps/Wolverhampton-Wanderers-Stats-All-Competitions"
    ]

    all_players = []

    # Loop through each team URL
    for url in team_urls:
        try:
            print(f"📥 Scraping: {url}")
            res = requests.get(url)
            soup = BeautifulSoup(res.content, "html.parser")
            time.sleep(3)

            # Extract the team name from the page header
            team_name = soup.find("h1").text.strip().replace(" Stats", "")

            # Get player data from this team's page
            players = get_player_info(soup, team_name)

            # Add this team's players to the full list
            all_players.extend(players)

        except Exception as e:
            print(f"❌ Failed to scrape {url}: {e}")

    # Convert list of all players into a single DataFrame
    df = pd.DataFrame(all_players)

    # Save to CSV in the /data folder
    df.to_csv("data/premier_league_2024_25.csv", index=False)
    print("✅ All Premier League player stats scraped and saved.")


# ============================
# Entry point: run scraper
# ============================
if __name__ == "__main__":
    scrape_all_teams()
