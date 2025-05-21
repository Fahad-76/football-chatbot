#
#  database.py
#  FBref Bot
#
#  Created by Fahad on 20/05/2025.
#
#  This module loads the player stats CSV file and provides a method
#  to search for a player's statistics by name.

import pandas as pd  # Used for loading and querying the CSV data

class PlayerStats:
    def __init__(self, csv_path="data/premier_league_2024_25.csv"):
        """
        Initializes the PlayerStats object by loading the CSV into a DataFrame.
        Normalizes player names to lowercase for easier matching.
        """
        try:
            self.df = pd.read_csv(csv_path)
            self.df["player"] = self.df["player"].str.lower()  # Normalize names for case-insensitive search
        except Exception as e:
            print(f"❌ Failed to load CSV: {e}")
            self.df = pd.DataFrame()  # Load empty DataFrame on failure to prevent crashes

    def get_stats(self, player_name):
        """
        Searches for the first player whose name contains the input string.
        Returns the player's row as a dictionary, or None if not found.
        """
        player_name = player_name.lower().strip()  # Normalize input for search
        matches = self.df[self.df["player"].str.contains(player_name)]

        if matches.empty:
            return None  # No player matched

        # Return the first match as a dictionary of stats
        return matches.iloc[0].to_dict()
