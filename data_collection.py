import html5lib
import requests
import lxml
from bs4 import BeautifulSoup
from bs4 import Comment
import pandas as pd
import numpy as np
pd.set_option('mode.chained_assignment', None)

#Getting the teams acronims
teams = pd.read_csv('mlb_teams_abbreviations.csv')
teams = list(teams.iloc[:,0])

# Get the roster table from the placeholder comment
def is_comment(element): 
    return isinstance(element, Comment)

dfs = []

for t in teams:
    url = 'https://www.baseball-reference.com/teams/'+t+'/2019.shtml'
    html = requests.get(url).content
    soup =  BeautifulSoup(html, 'html5lib')
    try:
        roster = soup.find(attrs={'id':'all_the40man'}).find(text=is_comment)
        man40 = pd.read_html(str(BeautifulSoup(roster, features="lxml").find(attrs={'id':'the40man'})))[0]
    except:
        continue
    #rosters = pd.read_html(str(BeautifulSoup(roster).find(attrs={'id':'the40man'})))[0]
    dfs.append(man40)
rosters = pd.concat(dfs)

#removing duplicate headers
rosters = rosters.drop(rosters[rosters['Rk'] == 'Rk'].index)

#Fixing missing column names, accordin to the website the 4th column correspond to the player country and the 5th supposed to be his role but is not very clear
#Chaging the names to be more clear
rosters.columns = ['Rk', 'number', 'name', 'country', 'role', 'active', 'injured', 'age',
                 'batting_side', 'throwing_hand', 'height', 'weight', 'birt_date', 'first_year']

#Removing Rk (rank) role columns
rosters.drop(['Rk','role'], axis=1, inplace=True)

#Removing the duplicate label on the country column
rosters['country'] = rosters['country'].str.split(expand=True)[1]

#Converting active and injured into binary classification 1 is injured, or active while 0 is not for any of them.
rosters['active'] = np.where(rosters['active'].isna(),0,1)
rosters['injured'] = np.where(rosters['injured'].isna(),0,1)

#Formmating the height. Height will be expressed in inches.
rosters['height'] = rosters['height'].str.split(expand=True)[0].str.replace("'",'').astype(int) * 12 + rosters['height'].str.split(expand=True)[1].str.replace('"','').astype(int)

# Converting weight to numeric
rosters['weight'] = pd.to_numeric(rosters['weight'])

# Convertin birth_date to date time format
rosters['birt_date'] = pd.to_datetime(rosters['birt_date'])

# There are some duplicated rows, I removed them:
rosters.drop_duplicates(inplace=True)

#Getting batting statistics
dfs = []

for t in teams:
    url = 'https://www.baseball-reference.com/teams/'+t+'/2018.shtml'
    html = requests.get(url).content
    soup =  BeautifulSoup(html, 'html5lib')
    try:
        bat = pd.read_html(str(soup.find(attrs={'id':'team_batting'})))[0]
    except:
        continue
    dfs.append(bat)
batting = pd.concat(dfs)

#Remove repeating headings
batting = batting.drop(batting[batting['Rk'] == 'Rk'].index)
#Remove the subtotal rows
batting = batting.drop(batting[batting['Rk'].isna()].index)
#Remove duplicated rows
batting.drop_duplicates(inplace=True)

#Joing both tables on names
df =  pd.merge(left=batting, right=rosters, how='inner', left_on='Name', right_on='name')

df = df[['age', 'batting_side', 'height', 'weight', 'first_year','G', 'PA', 'R', 'SB', 'SO', 'country', 'OPS']]

#Remove records with missing OPS
df.dropna(axis=0, inplace=True)

#Convert numerical values into integers
def change_num_type(dtf):    
    for c in list(dtf.columns):
        try:
            dtf[c] = dtf[c].astype(int)
        except:
            pass
change_num_type(df)

df['OPS'] = df['OPS'].astype(float)

df.columns = ['age', 'batting_side', 'height', 'weight', 'first_year', 
              'games_played', 'plates_appearances', 'runs',
               'stolen_bases', 'strike_outs', 'country', 'OPS']


#Splitting the dataset into train and test sets.

from sklearn.model_selection import train_test_split
y = df[['OPS']]
X = df.drop('OPS', axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=28)
train = pd.concat([X_train,y_train], axis=1)
test = pd.concat([X_test,y_test], axis=1)

train.to_csv('train.csv', index=False)
test.to_csv('test.csv', index=False)


