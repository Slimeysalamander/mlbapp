import streamlit as st
import requests
from datetime import datetime

# Function to get game PKs given a specific date
def get_game_pks(date):
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date.strftime('%Y-%m-%d')}"
    response = requests.get(url)
    
    if response.status_code == 200:
        games = response.json().get('dates', [])
        game_pks = []
        for date_info in games:
            for game in date_info.get('games', []):
                game_pks.append(game['gamePk'])
        return game_pks
    return []

# Function to get game details by gamePk
def get_game_details(game_pk):
    url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
    response = requests.get(url)
    
    if response.status_code == 200:
        game_data = response.json()
        game_info = game_data.get('gameData', {})
        teams = game_info.get('teams', {})
        
        home_team = teams.get('home', {}).get('name', 'N/A')
        away_team = teams.get('away', {}).get('name', 'N/A')
        
        return home_team, away_team
    else:
        return None, None

st.title("Team Search by Date")

# Get game PKs and team info by date
st.header("Lookup Teams by Date")
date_input = st.date_input("Select Game Date", value=datetime.today())

if st.button("Get Teams"):
    date = datetime.strptime(str(date_input), '%Y-%m-%d')
    game_pks = get_game_pks(date)

    if game_pks:
        # Get team info for the retrieved game PKs
        teams_info = []
        for game_pk in game_pks:
            home_team, away_team = get_game_details(game_pk)
            if home_team and away_team:
                teams_info.append(f"Game PK {game_pk}: Home Team - {home_team}, Away Team - {away_team}")
            else:
                teams_info.append(f"Game PK {game_pk}: No game found or error fetching details.")

        st.subheader("Teams Information:")
        for info in teams_info:
            st.write(info)
    else:
        st.write(f"No games found for {date.strftime('%Y-%m-%d')}.")