import html5lib
import requests
import lxml
from bs4 import BeautifulSoup
from bs4 import Comment
import pandas as pd
import numpy as np
from helpers import col_desc
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
pd.options.display.max_rows = 100
pd.options.display.max_columns = 100

# Get the roster table from the placeholder comment
def is_comment(element): 
    return isinstance(element, Comment)
url = 'https://www.baseball-reference.com/teams/ARI/2019.shtml'
html = requests.get(url).content
soup =  BeautifulSoup(html, 'html5lib')
roster = soup.find(attrs={'id':'all_the40man'}).find(text=is_comment)
man40 = pd.read_html(str(BeautifulSoup(roster, features="lxml").find(attrs={'id':'the40man'})))[0]

#removing duplicate headers
man40 = man40.drop(man40[man40['Rk'] == 'Rk'].index)

#Fixing missing column names, accordin to the website the 4th column correspond to the player country and the 5th supposed to be his role but is not very clear
#Chaging the names to be more clear
man40.columns = ['Rk', 'number', 'name', 'country', 'role', 'active', 'injured', 'age',
                 'batting_side', 'throwing_hand', 'height', 'weight', 'birt_date', 'first_year']

#Removing Rk (rank) role columns
man40.drop(['Rk','role'], axis=1, inplace=True)

#Removing the duplicate label on the country column
man40['country'] = man40['country'].str.split(expand=True)[1]

#Converting active and injured into binary classification 1 is injured, or active while 0 is not for any of them.
man40['active'] = np.where(man40['active'].isna(),0,1)
man40['injured'] = np.where(man40['injured'].isna(),0,1)

#Formmating the height. Height will be expressed in inches.
man40['height'] = man40['height'].str.split(expand=True)[0].str.replace("'",'').astype(int) * 12 + man40['height'].str.split(expand=True)[1].str.replace('"','').astype(int)

# Converting weight to numeric
man40['weight'] = pd.to_numeric(man40['weight'])

# Convertin birth_date to date time format
man40['birt_date'] = pd.to_datetime(man40['birt_date'])

#Getting batting and pitching statistics
batting = pd.read_html(str(soup.find(attrs={'id':'team_batting'})))[0]
pitching = pd.read_html(str(soup.find(attrs={'id':'team_pitching'})))[0]
#Remove repeating headings
batting = batting.drop(batting[batting['Rk'] == 'Rk'].index)
pitching = pitching.drop(pitching[pitching['Rk'] == 'Rk'].index)
#Remove the subtotal rows
batting = batting.drop(batting[batting['Rk'].isna()].index)
pitching = pitching.drop(pitching[pitching['Rk'].isna()].index)

#Selecting main statistics columns and Renaming them for easier interpretation:
batting = batting[['Pos', 'Name', 'G', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR', 'SB', 'CS', 'BB', 'SO']]
col_ren = ['position', 'name', 'games_played', 'plate_appearances', 'at bats', 'runs_made', 'hits_made', 
           'doubles-made','triples-made','home_runs-made','stolen_bases','caught_stealing','base_on_balls','strikes_out']
batting.columns = col_ren

#Getting the main statistics and renaming the columns
pitching = pitching[['Name', 'W', 'L', 'G', 'GS', 'GF', 'CG', 'SHO', 'SV', 'IP', 'H', 'R', 'ER', 'HR', 'BB', 'SO', 'HBP','BK', 'WP', 'BF']]
col_ren = ['name', 'wins', 'losses','games_pitched', 'games_started','games_finished', 'complete_game','shutouts','saves','innings_pitched','hits-allowed',
          'runs-allowed','earned_runs-allowed', 'home_runs-allowed','base_on_balls-allowed','strikeouts','times_hit_by_pitch','balks','wild_pitches','batters_faced']
pitching.columns = col_ren

#Creating the main data set using player name as primary key
df = pd.merge(pd.merge(man40, batting, left_on='name', right_on='name', how='left'), pitching, left_on='name', right_on='name', how='left')

df.to_csv('roster_data.csv', index=False)