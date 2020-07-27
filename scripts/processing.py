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
        appe = soup.find(attrs={'id':'all_appearances'}).find(text=is_comment)
        roster = pd.read_html(str(BeautifulSoup(appe, features="lxml").find(attrs={'id':'appearances'})))[0]
    except:
        continue
    #rosters = pd.read_html(str(BeautifulSoup(roster).find(attrs={'id':'the40man'})))[0]
    dfs.append(roster)

roster = pd.concat(dfs)


#---------------------------------------------------------------------------
roster = roster.drop(roster[roster['Age'] == 'Age'].index)

#Renaming the columns
newColsNames = {'Name':'name', 'Age':'age','Unnamed: 2':'country','B':'batting_side','T':'throwing_hand','Ht':'height',
                'Wt':'weight', 'DoB':'date_of_birth','Yrs':'years','Salary':'salary', 'Batting':'batting'}
roster.rename(newColsNames, axis=1, inplace=True)
roster = roster[['name', 'age', 'country', 'batting_side', 'height', 'weight', 'years', 'batting','salary']]

#Country is duplicated on the same column. Getting only one instance.
roster['country'] = roster['country'].str.split(expand=True)[1]

#Converting height into total inches.
roster['height'] = roster['height'].str.split(expand=True)[0].str.replace("'",'').astype(int) * 12 + roster['height'].str.split(expand=True)[1].str.replace('"','').astype(int)
roster['weight'] = pd.to_numeric(roster['weight'])
roster['salary'] = roster['salary'].str.replace('$','').str.replace(',','').astype(float)
# There are some duplicated rows, I removed them:
roster.drop_duplicates(inplace=True)


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
df =  pd.merge(left=batting, right=roster, how='inner', left_on='Name', right_on='name')

df = df[['age', 'country','batting_side', 'height', 'weight', 'year','salary','batting','G', 'PA', 'R', 'SB', 'SO', 'OPS']]

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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=52)
train = pd.concat([X_train,y_train], axis=1)
test = pd.concat([X_test,y_test], axis=1)

train.to_csv('train.csv', index=False)
test.to_csv('test.csv', index=False)


