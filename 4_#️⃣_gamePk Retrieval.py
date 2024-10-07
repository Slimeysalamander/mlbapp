import streamlit as st
import requests
from datetime import datetime

# Function to get gamepk given a specific date
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

st.title("gamePk Search for use with 'gamePk to Team Info' page")

# Stores user input for the date
date_input = st.date_input("Select Game Date", value=datetime.today())

# Button that when pressed shows game Pks
if st.button("Get gamePk's"):
    date = datetime.strptime(str(date_input), '%Y-%m-%d')  # Convert date input to datetime
    game_pks = get_game_pks(date)

    if game_pks:
        st.header(f"gamePk's on {date.strftime('%Y-%m-%d')}:")
        for game_pk in game_pks:
            st.write(game_pk)
    else:
        st.write(f"No games found for {date.strftime('%Y-%m-%d')}.")
