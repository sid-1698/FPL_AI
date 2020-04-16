import pandas as pd 
import os 
import writer


def check(player_name,season,data):
    if player_name in data['Name'].values:
        ind = data[data['Name'] == player_name].index[0]
        if season in data.loc[ind,'Seasons']:
            return [2,data]
        data.loc[ind,'Seasons'] = str(data.loc[ind,'Seasons']) + season + ' | '
        data.loc[ind,'Total'] = data.loc[ind,'Total'] + 1
        return [1,data]
    else:
        data.loc[len(data),'Name'] = player_name
        data.loc[len(data)-1,'Seasons'] = '| ' + str(season) + ' | '
        data.loc[len(data)-1,'Total'] = 1
        return [0,data]


def update(existing_data,data,flag):
    if flag == 0:
        return data
    elif flag == 1:
        new_data = pd.concat([existing_data,data],ignore_index = True)
        return new_data
    




