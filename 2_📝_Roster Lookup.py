import streamlit as st
import statsapi
import requests

# Function that gets the team ID by name
def get_team_id(team_name):
    url = "https://statsapi.mlb.com/api/v1/teams"
    response = requests.get(url)
    
    if response.status_code == 200:
        teams = response.json().get('teams', [])
        for team in teams:
            if team_name.lower() in team['name'].lower():
                return team['id'], team['name']
    return None, None

# Function that gets the roster for a specific team and season
def get_team_roster(team_id, season):
    url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster"
    response = requests.get(url)
    
    if response.status_code == 200:
        roster_data = response.json()
        return roster_data.get('roster', [])
    return []

st.title("Team Roster Lookup by Season")

# User input for team name and season
team_name = st.text_input("Please Enter Team Name")
season = st.number_input("Please Enter Season (ex: 2024)", min_value=1900, max_value=2100, value=2024)

# Button to show you the roster once set up
if st.button("Get Roster"):
    if team_name:
        team_id, full_team_name = get_team_id(team_name)
        
        if team_id:
            roster = get_team_roster(team_id, season)
            if roster:
                st.header(f"{full_team_name} Roster for {season}")
                for player in roster:
                    player_name = player['person']['fullName']
                    position = player['position']['name']
                    st.write(f"{player_name} - Position: {position}")
            else:
                st.write(f"No roster found for {full_team_name} in {season}.")
        else:
            st.write(f"Team '{team_name}' not found.")
    else:
        st.write("Please enter a team name.")