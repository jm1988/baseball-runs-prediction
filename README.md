## Overview

The goal of this project is to predict the OPS for a particular baseball player in a given season. 

from [wikipedia](https://en.wikipedia.org/wiki/On-base_plus_slugging):

"*On-base plus slugging (OPS) is a sabermetric baseball statistic calculated as the sum of a player's on-base percentage and slugging percentage.[1] The ability of a player both to get on base and to hit for power, two important offensive skills, are represented. An OPS of .900 or higher in Major League Baseball puts the player in the upper echelon of hitters. Typically, the league leader in OPS will score near, and sometimes above, the 1.000 mark.*" 

Using different caracteristics from a player like age, height, weight, etc. And his previous year stats; like runs, plates appearances, among others.

The analysis only consider active batters.

## Data Processing

- ### Collection

    The data was scraped from the [baseball-reference](https://www.baseball-reference.com/teams/TOR/2019.shtml) website. Specifically from the stats section for every MLB team.

    Only 2 tables were used: the Team Batting and the Current 40-Man Roster. The data was obtained for every available team, then cleaned and merge.

- ### Cleaning

    The records with available OPS were the only considered for this project, any row missing this variable was removed. Columns were renamed for easier interpretation. Total and subtotals rows were removed, and also any duplicate record was deleted.
    
    For the current version of this analysis the only columns used are: age, batting_side, height, weight, first_year, games_played, plates_appearances, runs, stolen_bases, strike_outs, country and, of course, OPS.
    
    Both tables were merged using an inner join.


- ### Datasets Split
    The processed data them was split into test and training set. To avoid bias in the analysis.
    
The script used for this part is available in this repository.

## Exploratory Data Analysis