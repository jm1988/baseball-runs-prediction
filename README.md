## Overview

The goal of this project is to predict the number of runs for a particular baseball player in a given season. 

Using different caracteristics from a player like age, height, weight, etc. And other stats.

The analysis only consider active batters.

## Data Processing

- ### Collection

    The data was scraped from the [baseball-reference](https://www.baseball-reference.com/teams/TOR/2019.shtml) website. Specifically from the stats section for every MLB team.

    Only 2 tables were used: the Team Batting and the Current 40-Man Roster. The data was obtained for every available team, then cleaned and merge.

- ### Cleaning

    The records with available runs were the only considered for this project, any row missing this variable was removed. Columns were renamed for easier interpretation. Total and subtotals rows were removed, and also any duplicate record was deleted.
    
    Both tables were merged using an inner join.


- ### Datasets Split
    The processed data them was split into test and training set. To avoid bias in the analysis.
    
The script used for this part is available in this repository.

## Exploratory Data Analysis

In this step the data was explored to check for pattern, distributions and correlation between the variables. There seems to be high colinearity between the independent variables.
