from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, playergamelog
import pandas as pd
import time
import sys

# Function to find a player's ID from their full name.
# The nba_api uses a unique ID for each player, so this is the first step.
def find_player_id(full_name):
    """
    Finds a player's ID by their full name.
    
    Args:
        full_name (str): The full name of the player (e.g., 'LeBron James').
    
    Returns:
        int: The unique player ID if found, otherwise None.
    """
    try:
        nba_players = players.get_players()
        # Search for the player using a list comprehension.
        player_info = [
            player for player in nba_players 
            if player['full_name'].lower() == full_name.lower()
        ]
        
        if player_info:
            return player_info[0]['id']
        else:
            print(f"Error: Player '{full_name}' not found.")
            return None
    except Exception as e:
        print(f"An error occurred while fetching player list: {e}")
        return None

# Function to get a player's career statistics.
def get_career_stats(player_id):
    """
    Retrieves a player's career regular season statistics.

    Args:
        player_id (int): The unique player ID.

    Returns:
        pd.DataFrame: A DataFrame containing the player's career stats, or an empty DataFrame on error.
    """
    try:
        print("Fetching career stats...")
        # Make the API call and get the career stats.
        career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
        # Convert the API response into a pandas DataFrame.
        # The API returns a list of dataframes; we want the first one, which is the overall stats.
        career_df = career_stats.get_data_frames()[0]
        return career_df
    except Exception as e:
        print(f"An error occurred while fetching career stats: {e}")
        return pd.DataFrame()

# Function to get a player's game logs for a specific season.
def get_game_logs(player_id, season_year):
    """
    Retrieves a player's game logs for a specific season.

    Args:
        player_id (int): The unique player ID.
        season_year (str): The season in 'YYYY-YY' format (e.g., '2023-24').

    Returns:
        pd.DataFrame: A DataFrame containing the player's game logs, or an empty DataFrame on error.
    """
    try:
        print(f"Fetching game logs for the {season_year} season...")
        # Make the API call and get the game logs.
        # It's good practice to add a small delay to avoid hitting API rate limits.
        time.sleep(1)
        game_logs = playergamelog.PlayerGameLog(player_id=player_id, season=season_year)
        # Convert the API response into a pandas DataFrame.
        # We handle the possibility of an empty result set.
        game_log_df = game_logs.get_data_frames()[0]
        return game_log_df
    except Exception as e:
        print(f"An error occurred while fetching game logs: {e}")
        return pd.DataFrame()

# Main script execution logic.
if __name__ == "__main__":
    # Define the player and season you want to track.
    player_name = 'Alaa Abdelnaby'  # You can change this to any player
    season = '2023-24'            # You can change this to any valid season

    # Find the player's ID.
    player_id = find_player_id(player_name)
    
    # Only proceed if the player ID was successfully found.
    if player_id:
        # Get and print career stats.
        career_df = get_career_stats(player_id)
        if not career_df.empty:
            print(f"\n--- {player_name} Career Statistics ---")
            print(career_df)

        # Get and print game logs for the specified season.
        game_log_df = get_game_logs(player_id, season)
        if not game_log_df.empty:
            print(f"\n--- {player_name} Game Logs ({season} Season) ---")
            print(game_log_df)

        if career_df.empty and game_log_df.empty:
            print("\nNo data retrieved. Please check the player name and season.")
