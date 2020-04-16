import scraper
import merger
import writer
import cleaner
import imputer
import global_merger

import sys
import os
from datetime import datetime
import pandas as pd 
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def main(argv):

    path = 'C:/Users/sidsu/Downloads/FPL_AI/Data/'
    path = path+argv[1]+'/'


    fpl = scraper.fpl_scraper('https://fantasy.premierleague.com/api/bootstrap-static/')
    fbref = scraper.fbref_scraper('https://fbref.com/en/comps/9/stats/Premier-League-Stats')

    fpl.get_data()
    fbref.get_data()

    writer.write(fpl.players_data,path,'Fpl_Players.xlsx')
    writer.write(fbref.players_data,path,'Fbref_Players.xlsx')
    writer.write(fpl.teams_data,path,'Fpl_Teams_data.xlsx')
    writer.write(fbref.teams_data,path,'Fbref_Teams_data.xlsx')

    players = merger.overall_data(fpl.players_data,fbref.players_data)
    teams = merger.teams_data(fpl.teams_data,fbref.teams_data)

    players = cleaner.overall_data(players)
    teams = cleaner.teams_data(teams)

    writer.write(players,path,'Players.xlsx')
    writer.write(teams,path,'Teams.xlsx')

    players_data = pd.read_excel('C:/Users/sidsu/Downloads/FPL_AI/Data/Players.xlsx',index_col=0)
    cnt = 0
    for ind,row in players.iterrows():

        [flag,players_data] = global_merger.check(row['Name'],argv[1],players_data)

        url = 'https://fbref.com'+row['Url']
        api = "https://fantasy.premierleague.com/api/element-summary/"+str(row['Id'])+'/'

        fpl_players = scraper.fpl_scraper(api)
        fbref_players = scraper.fbref_scraper(url)

        fpl_players.get_inidividual_data()
        fbref_players.get_individual_data()

        if fbref_players.fail == 0:
            for col in ['xg','npxg','xa']:
                if col not in fbref.individual_data.columns:
                    fbref.individual_data[col] = np.nan

            player_data = merger.player_data(fpl_players.individual_data,fbref_players.individual_data)
            player_data = cleaner.player_data(player_data)
            player_data = imputer.impute(player_data)
            player_data = imputer.feature_engineering(player_data,row['Team'],teams)

            writer.write(player_data,path+'Individual_Player_Data/',row['Name'].replace(' ','_')+'.xlsx',0)
    
            global_merger.update(row['Name'].replace(' ','_')+'.xlsx',player_data,flag,cnt)
            cnt += 1

        else:
            players = players.drop(ind,axis=0)

    writer.write(players,path,"Players.xlsx")
    writer.write(players_data,'C:/Users/sidsu/Downloads/FPL_AI/Data/','Players.xlsx',1)

if __name__ == "__main__":
    main(sys.argv)