import scraper
import merger
import writer
import cleaner
import imputer
import global_merger

import sys
import os
import datetime
import pandas as pd 
import numpy as np
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

def main(argv):

    master_path = Path(os.path.dirname(os.path.abspath(__file__))) / "Data"
    path = master_path / argv[1]

    fpl_season_start_date = datetime.datetime.strptime('2020-08-08','%Y-%d-%m').date()

    if datetime.date.today() < fpl_season_start_date:

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
    
    else:
        players = pd.read_excel(path/'Players.xlsx',index_col=0)
        teams = pd.read_excel(path/'Teams.xlsx',index_col=0)

    players_data = pd.read_excel(master_path/'Players_Master.xlsx',index_col=0)
    cnt = 1
    for ind,row in players.iterrows():

        [flag,players_data] = global_merger.check(row['Name'].replace(' ','_'),argv[1],players_data)
        url = 'https://fbref.com'+row['Url']
        api = "https://fantasy.premierleague.com/api/element-summary/"+str(row['Id'])+'/'
        filename = row['Name'].replace(' ','_') + '.xlsx'

        fpl_players = scraper.fpl_scraper(api)
        fbref_players = scraper.fbref_scraper(url)

        fpl_players.get_inidividual_data()
        fbref_players.get_individual_data()

        if fbref_players.fail == 0:
            for col in ['xg','npxg','xa']:
                if col not in fbref_players.individual_data.columns:
                    fbref_players.individual_data[col] = np.nan

            player_data = merger.player_data(fpl_players.individual_data,fbref_players.individual_data)
            player_data = cleaner.player_data(player_data)
            player_data = imputer.impute(player_data)
            player_data = imputer.feature_engineering(player_data,row['Team'],teams)

            writer.write(player_data,path/'Individual_Player_Data/',filename,cnt)
    
            if flag != 2:
                existing_data = pd.read_excel(master_path/'Master_Data'/filename)
                merged_player_data = global_merger.update(existing_data,player_data,flag)
                writer.write(merged_player_data,master_path/'Master_Data/',filename,cnt)
                cnt += 1
        else:
            players = players.drop(ind,axis=0)

    writer.write(players,path,"Players.xlsx")
    writer.write(players_data,master_path,'Players_Master.xlsx')

if __name__ == "__main__":
    main(sys.argv)