import pandas as pd 
import os 
import writer


def check(player_name,season,data):
    if player_name in data['Name'].values:
        ind = data[data['Name'] == player_name].index[0]
        data.loc[ind,'Seasons'] = str(data.loc[ind,'Seasons']) + season + ' | '
        data.loc[ind,'Total'] = data.loc[ind,'Total'] + 1
        return [1,data]
    else:
        data.loc[len(data),'Name'] = player_name
        data.loc[len(data)-1,'Seasons'] = '| ' + str(season) + ' | '
        data.loc[len(data)-1,'Total'] = 1
        return [0,data]


def update(file,data,flag,cnt):
    path = 'C:/Users/sidsu/Downloads/FPL_AI/Data/Master_Data/'
    if flag == 0:
        writer.write(data,path,file,cnt)
    else:
        existing_data = pd.read_excel(path+file,index_col=0)
        new_data = pd.concat([existing_data,data],ignore_index = True)
        writer.write(new_data,path,file,cnt)
    




