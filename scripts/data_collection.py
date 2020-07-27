import html5lib
import requests
import lxml
from bs4 import BeautifulSoup
from bs4 import Comment
import pandas as pd
import numpy as np
pd.set_option('mode.chained_assignment', None)

#Getting the teams acronyms
teams = pd.read_csv('../data/mlb_teams_abbreviations.csv')
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
    
    dfs.append(roster)

roster = pd.concat(dfs)

#Getting batting statistics
dfs = []

for t in teams:
    url = 'https://www.baseball-reference.com/teams/'+t+'/2019.shtml'
    html = requests.get(url).content
    soup =  BeautifulSoup(html, 'html5lib')
    try:
        bat = pd.read_html(str(soup.find(attrs={'id':'team_batting'})))[0]
    except:
        continue
    dfs.append(bat)
batting = pd.concat(dfs)

#saving the collected data as csv files.

roster.to_csv('../data/roster_raw.csv', index=False)
batting.to_csv('../data/batting_raw.csv', index=False)