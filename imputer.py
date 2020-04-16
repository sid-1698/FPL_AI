import pandas as pd 
import os

def calc_strength_diff(curr_team,opp_team,teams,was_home,column):
    if column == 'Strength':
        return teams[teams['Id'] == curr_team][column].values[0] - teams[teams['Id'] == opp_team][column].values[0]
    else:
        if was_home == 1:
            return teams[teams['Id'] == curr_team][column+'H'].values[0] - teams[teams['Id'] == opp_team][column+'A'].values[0]
        else:
            return teams[teams['Id'] == curr_team][column+'A'].values[0] - teams[teams['Id'] == opp_team][column+'H'].values[0]

def feature_engineering(data,team,teams):
    data['GD'] = data.apply(lambda row : row['Home_Score'] - row['Away_Score'] if row['Venue'] == True else row['Away_Score'] - row['Home_Score'],axis=1)

    for item in ['Strength','SO','SA','SD']:
        data[item] = data.apply(lambda row : calc_strength_diff(team,row['Opponent'],teams,row['Venue'],item),axis=1)      

    return data

def impute(data):

    for item in ['Starting11','Minutes','Assists','Shots','On_Target','Crosses','Fouls','Fouled','Tackles','Penalties_Scored','Penalties_Missed','Penalties_Saved','Interceptions','Yellow_Cards','Red_Cards','Goals_Scored','Influence','Creativity','Threat','ICT_Index','BPS','Bonus','Total_Points']:
        data[item].fillna(0,inplace=True)

    data.dropna(axis=0,how='any',subset=['Away_Score','Home_Score','Opponent','Venue'],inplace=True)

    return data



if __name__ == "__main__":
    pass