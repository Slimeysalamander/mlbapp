import streamlit as st
import requests

# Function to get game details by gamePk
def get_game_details(game_pk):
    url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
    response = requests.get(url)
    
    if response.status_code == 200:
        game_data = response.json()
        game_info = game_data.get('gameData', {})
        teams = game_info.get('teams', {})
        
        home_team = teams.get('home', {}).get('name')
        away_team = teams.get('away', {}).get('name')
        
        return home_team, away_team
    else:
        return None, None

# Streamlit app layout
st.title("Team Info Using gamePk")

# User input for the gamePk
game_pk_input = st.number_input("Enter gamePk:", min_value=1, step=1)

# Button to fetch game details
if st.button("Get Teams"):
    home_team, away_team = get_game_details(game_pk_input)
    
    if home_team and away_team:
        st.header("Teams Played:")
        st.write(f"Home Team: {home_team}")
        st.write(f"Away Team: {away_team}")
    else:
        st.write("Error fetching game details. Please check the Game PK.")