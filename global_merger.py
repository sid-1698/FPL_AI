import pandas as pd 
import os 
import writer


def check(player_name,season):
    path = 'C:/Users/sidsu/Downloads/FPL_AI/Data/'
    data = pd.read_excel(path+'Players.xlsx')
    if player_name in data['Name'].values:
        ind = data[data['Name'] == player_name].index[0]
        data.loc[ind,'Seasons'] = str(data.loc[ind,'Seasons']) + season + ' | '
        data.loc[ind,'Total'] = data.loc[ind,'Total'] + 1
        writer.write(data,path,'Players.xlsx',0)
        return 1
    else:
        data.loc[len(data),'Name'] = player_name
        data.loc[len(data),'Season'] = '| ' + season + ' | '
        data.loc[len(data),'Total'] = 1
        writer.write(data,path,'Players.xlsx',0)
        return 0


def update(file,data,flag):
    path = 'C:/Users/sidsu/Downloads/FPL_AI/Data/Master_Data/'
    if flag == 0:
        writer.write(data,path,file+'.xlsx')
    else:
        existing_data = pd.read_excel(path+file+'.xlsx')
        new_data = pd.concat([existing_data,data],ignore_index = True)
        writer.write(new_data,path,file+'.xlsx')
    




