import pandas as pd 
from bs4 import BeautifulSoup
import requests
import time

url = 'https://fbref.com/en/comps/9/Premier-League-Stats'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

#general stats
standings_table = soup.find_all('table')
teams = standings_table[2]
standard_stats_df = pd.read_html(str(teams))[0]
team_col = standard_stats_df.iloc[:, 0:1]
team_col = pd.concat([team_col, standard_stats_df.iloc[:, 2:17]], axis = 1)

#shooting stats
shooting_table = soup.find_all('table')
shooting_teams = shooting_table[8]
shooting_table_df = pd.read_html(str(shooting_teams))[0]
shooting_teams_col = pd.concat([team_col.reset_index(drop=True), shooting_table_df.iloc[:, 4:15]], axis = 1)

#general passing stats
passing_table = soup.find_all('table')
passing_teams = passing_table[10]
passing_table_df = pd.read_html(str(passing_teams))[0]
passing_teams_col = pd.concat([team_col.reset_index(drop=True), passing_table_df.iloc[:, 3:8]], axis = 1)

#passing type stats
passing_type_table = soup.find_all('table')
passing_type_teams = passing_type_table[12]
passing_type_table_df = pd.read_html(str(passing_type_teams))[0]
passing_type_table_col = pd.concat([team_col.reset_index(drop=True), passing_type_table_df.iloc[:, 4:12]], axis = 1)

all_data = team_col.merge(shooting_teams_col)
all_data = all_data.merge(passing_teams_col)
all_data = all_data.merge(passing_type_table_col)
all_data.columns = all_data.columns.droplevel()
all_data.insert(0, "Position", [1, 4, 13, 15, 10, 19, 9, 14, 16, 12, 3, 18, 2, 7, 6, 17, 20, 5, 8, 11], True)
final = all_data.rename(columns = {'Poss': 'Possession', 
    'MP': 'Matches Played', 
    'Gls': 'Goals', 
    'Ast': 'Assists', 
    'G+A': 'Goals + Assists', 
    'G-PK': 'Non-Pen Goals', 
    'PK': 'Penalties', 
    'PKatt': 'Penalties Attempted', 
    'CrdY': 'Yellows', 
    'CrdR': 'Reds', 
    'Sh': 'Shots', 
    'SoT': 'Shots on Target',
    'SoT%': 'Shot Accuracy Percentage',
    'Sh/90': 'Shots per 90 Minutes',
    'SoT/90': 'Shots on Target per 90 Minutes',
    'G/Sh': 'Goals per Shot',
    'G/SoT': 'Goals per Shot on Target',
    'Dist': 'Distance Covered (Yards)',
    'FK': 'Free Kicks Taken',
    'TB': 'Through Balls',
    'Sw': 'Successful Dribbles',
    'Crs': 'Crosses',
    'TI': 'Tackles Attempted (Interceptions)',
    'CK': 'Corner Kicks'})
final.to_csv(r'C:\Users\Michelle Logue\Documents\Michael\Prem Data\Brighton-Data\Premier League Team Data.csv', index=False)
#'https://fbref.com/en/comps/9/Premier-League-Stats'
urls = ['https://fbref.com/en/comps/9/Premier-League-Stats',
        'https://fbref.com/en/comps/24/Serie-A-Stats',
        'https://fbref.com/en/comps/21/Primera-Division-Stats',
        'https://fbref.com/en/comps/23/Eredivisie-Stats',
        'https://fbref.com/en/comps/32/Primeira-Liga-Stats'
        ]
all_teams_data=[]
for u in urls:
    team_page = requests.get(u)
    soups = BeautifulSoup(team_page.text, 'html.parser')
    all_tables = soups.select('table.stats_table')[0]
    links = all_tables.find_all('a')
    links = [l.get("href") for l in links]
    links = [l for l in links if '/squads/' in l]

    team_urls = [f"https://fbref.com{l}" for l in links]
    for team_url in team_urls:
        team_page = requests.get(team_url)
        soups = BeautifulSoup(team_page.text, 'html.parser')
        shooting_table_1 = soups.find_all('table')
        if not shooting_table_1:
            print('Error with table')
        else:
            my_table = shooting_table_1[7]
            individ_data_list = pd.read_html(str(my_table))[0]
            all_teams_data.append(individ_data_list)
            time.sleep(1)

combined = pd.concat(all_teams_data, axis = 0, ignore_index = True)
combined.columns = combined.columns.droplevel()
combined = combined[combined['Player'].str.contains('Squad Total|Opponent Total') == False]
combined = combined.rename(columns = {'Player': 'Player Name',
    'Nation': 'Player Nationality',
    'Pos': 'Player Position',
    'Age': 'Player Age',
    '90s': '90 Minutes Played',
    'SCA': 'Shot-Creating Actions (SCA)',
    'SCA90': 'Shot-Creating Actions per 90 Minutes',
    'PassLive': 'Passes Leading to Shot-Creating Actions (Live)',
    'PassDead': 'Passes Leading to Shot-Creating Actions (Dead)',
    'TO': 'Through Balls Leading to Shot-Creating Actions',
    'Sh': 'Shots Leading to Shot-Creating Actions',
    'Fld': 'Fouls Leading to Shot-Creating Actions',
    'Def': 'Defensive Actions Leading to Shot-Creating Actions',
    'GCA': 'Goal-Creating Actions (GCA)',
    'GCA90': 'Goal-Creating Actions per 90 Minutes',
    'PassLive': 'Passes Leading to Goal-Creating Actions (Live)',
    'PassDead': 'Passes Leading to Goal-Creating Actions (Dead)',
    'TO': 'Through Balls Leading to Goal-Creating Actions',
    'Sh': 'Shots Leading to Goal-Creating Actions',
    'Fld': 'Fouls Leading to Goal-Creating Actions',
    'Def': 'Defensive Actions Leading to Goal-Creating Actions',
    'Matches': 'Matches Played'})

import re
pattern = r'[^a-zA-Z\s]'
combined_stats = combined['Player Name'].str.replace(pattern, '', regex=True)
combined_stats1 = combined_stats.tolist()
#combined.insert(1, 'Player Name', combined_stats1, True)
combined.insert(0,'Player Named', combined_stats1)
del combined[combined.columns[1]]
combined.to_csv(r'C:\Users\Michelle Logue\Documents\Michael\Prem Data\Brighton-Data\Player Data.csv', errors = 'ignore', index = False)
