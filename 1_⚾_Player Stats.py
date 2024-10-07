import streamlit as st
import statsapi


st.title("Player Stats")

# Input for use to type player name
player_name = st.text_input("Enter Player Name (ex. John Smith)")

# Search for and retrieve stats
if player_name:
    players = statsapi.lookup_player(player_name)
    
    if players:
        player = players[0]  # Use the first name and assume it's the right one
        player_id = player['id']
        stats = statsapi.player_stat_data(player_id)
        
        st.write(f"Player: {player['fullName']}")
        st.json(stats)
    else:
        st.write("Player not found.")