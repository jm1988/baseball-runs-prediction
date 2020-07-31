import pandas as pd
import numpy as np
pd.set_option('mode.chained_assignment', None)


# Loading rosters data set
roster = pd.read_csv('../data/roster_raw.csv')

#Remove repeating headers:
roster = roster.drop(roster[roster['Age'] == 'Age'].index)

#Removing unwanted columns
roster.drop(['G','DoB','Batting', 'Defense','P','C','1B','2B','3B','SS','LF','CF','RF','OF',
            'DH','PH','PR','WAR','Unnamed: 28'], axis=1, inplace=True)

#Renaming the columns
newColsNames = {'Name':'name', 'Age':'age','Unnamed: 2':'country','GS':'games_started','B':'batting_side','T':'throwing_hand','Ht':'height',
                'Wt':'weight', 'Yrs':'years','Salary':'salary', 'Batting':'batting'}
roster.rename(newColsNames, axis=1, inplace=True)

#Country is duplicated on the same column. Getting only one instance.
roster['country'] = roster['country'].str.split(expand=True)[1]

#Converting height into total inches.
roster['height'] = roster['height'].str.split(expand=True)[0].str.replace("'",'').astype(int) * 12 + roster['height'].str.split(expand=True)[1].str.replace('"','').astype(int)
roster['weight'] = pd.to_numeric(roster['weight'])
roster['salary'] = roster['salary'].str.replace('$','').str.replace(',','').astype(float)
# There are some duplicated rows, I removed them:
roster.drop_duplicates(inplace=True)

#Loading batting data set
batting = pd.read_csv('../data/batting_raw.csv')
#Remove repeating headings
batting = batting.drop(batting[batting['Rk'] == 'Rk'].index)
#Remove the subtotal rows
batting = batting.drop(batting[batting['Rk'].isna()].index)
#Remove duplicated rows
batting.drop_duplicates(inplace=True)



batting.drop(['Rk','G', 'PA', 'AB', 'Age','H','2B','3B','HR','BA','OBP','SLG','OPS','OPS+','GDP','RBI'], axis=1, inplace=True)


new_col_names = {'Pos':'position', 'Name':'name', 'R':'runs','TB':'total_bases',
                'SB':'stolen_bases', 'CS':'caught_stealing','BB':'bases_on_balls', 
                'SO':'strikeouts', 'HBP':'hit_by_pitch','SH':'sacrafice_hits', 
                'SF':'sacrafice_flies', 'IBB':'intentional_bases_on_balls'}

batting.rename(new_col_names, axis=1, inplace=True)


#Replacing positions by their full name.
pos={"C":"Catcher", "1B":"First Base", "2B":"Second Base", "3B":"Third Base", "SS":"Short Stop",
        "LF":"Left Field", "CF":"Center Field", "RF":"Right Field","DH":"Designated Hitter",
        "SP":"Starting Pitcher","RP":"Relief Pitcher",}

batting['position'] = batting['position'].map(pos)



#Using a left join on names to merge both tables. This is because the label (runs) is on the batting data set (left table in the join)
df =  pd.merge(left=roster, right=batting, how='inner', left_on='name', right_on='name')


#Remove records with missing OPS (the variable of interest)
df.dropna(axis=0, inplace=True)

#replace 1st with one 1 in experience years
df['years'] = df['years'].str.replace('1st','1')

#Change the name of countries to the full name.
cc = pd.read_csv('../data/countries_codes.csv')
cc = cc.set_index('code').to_dict()['country']
df['country'] = df['country'].map(cc)

#Splitting the dataset into train and test sets.
from sklearn.model_selection import train_test_split
y = df[['salary']]
X = df.drop('salary', axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=52)
train = pd.concat([X_train,y_train], axis=1)
test = pd.concat([X_test,y_test], axis=1)

#Saving the clean data sets
train.to_csv('../data/train.csv', index=False)
test.to_csv('../data/test.csv', index=False)