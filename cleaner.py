import pandas as pd
import numpy as np
pd.set_option('display.max_columns',None)

def overall_data(data):
    data = data[['id','name','team','element_type','nationality','news','now_cost','web_name','matches']]
    
    for item in ['id','team','element_type','now_cost']:
        data[item] = pd.to_numeric(data[item],errors='coerce')

    data['nationality'] = data['nationality'].apply(lambda x : x.split(' ')[-1])
    data.columns = ['Id','Name','Team','Position_Code','Nationality','News','Cost','Web_Name','Url']

    return data

def teams_data(data):
    data = data[['id','name','strength','strength_overall_home','strength_overall_away','strength_attack_home','strength_attack_away','strength_defence_home','strength_defence_away','players_used','goals_per90','assists_per90','goals_pens_per90']]

    for item in data.columns:
        if item != 'name':
            data[item] = pd.to_numeric(data[item],errors='coerce')

    data.columns=['Id','Name','Strength','SOH','SOA','SAH','SAA','SDH','SDA','Players','Goals/90','Assists/90','Goals_Pens/90']
 
    return data

def player_data(data):
    try:
        data = data[['kickoff_time','round','game_started','minutes','assists','shots_total','shots_on_target','crosses','fouls','fouled',
                     'tackles_won','pens_made','penalties_missed','penalties_saved','saves','shots_on_target_against','interceptions',
                     'cards_yellow','cards_red','goals_scored','goals_conceded','influence','creativity','threat','ict_index',
                     'team_a_score','team_h_score','was_home','opponent_team','xg','npxg','xa','bps','bonus','total_points']]
        data.columns = ['Kickoff_Time','Gameweek','Starting11','Minutes','Assists','Shots','On_Target','Crosses','Fouls','Fouled','Tackles',
                        'Penalties_Scored','Penalties_Missed','Penalties_Saved','Saves','On_Target_Saves','Interceptions','Yellow_Cards','Red_Cards',
                        'Goals_Scored','Goals_Conceded','Influence','Creativity','Threat','ICT_Index','Away_Score','Home_Score','Venue','Opponent','xG','npxG',
                        'xA','BPS','Bonus','Total_Points']

    except:
        data = data[['kickoff_time','round','game_started','minutes','assists','shots_total','shots_on_target','crosses','fouls','fouled',
                     'tackles_won','pens_made','penalties_missed','penalties_saved','interceptions',
                     'cards_yellow','cards_red','goals_scored','goals_conceded','influence','creativity','threat','ict_index',
                     'team_a_score','team_h_score','was_home','opponent_team','xg','npxg','xa','bps','bonus','total_points']]
        data.columns = ['Kickoff_Time','Gameweek','Starting11','Minutes','Assists','Shots','On_Target','Crosses','Fouls','Fouled','Tackles',
                        'Penalties_Scored','Penalties_Missed','Penalties_Saved','Interceptions','Yellow_Cards','Red_Cards',
                        'Goals_Scored','Goals_Conceded','Influence','Creativity','Threat','ICT_Index','Away_Score','Home_Score','Venue','Opponent',
                        'xG','npxG','xA','BPS','Bonus','Total_Points']

    data['Kickoff_Time'] = pd.to_datetime(data['Kickoff_Time'],format='%Y-%m-%dT%H:%M:%SZ')
    data['Kickoff_Time'] = data['Kickoff_Time'].apply(lambda x : x.date())

    data['Starting11'] = data['Starting11'].apply(lambda x : 1 if x == 'Y' else 0)
    data['Venue'] = data['Venue'].apply(lambda x : 1 if x == True else 0)

    for item in data.columns:
        if item != 'Kickoff_Time':
            data[item] = pd.to_numeric(data[item],errors='raise')

    return data
    

if __name__ == "__main__":
    pass