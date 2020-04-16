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
    path = path+argv[1]+'/Individual_Player_Data/'
    players_data = pd.read_excel('C:/Users/sidsu/Downloads/FPL_AI/Data/Players.xlsx',index_col=0)
    cnt = 0
    for file in os.listdir(path):
        name = file.split('.')[0]
        [flag,players_data] = global_merger.check(name,argv[1],players_data)
        data = pd.read_excel(path+file,index_col=0)
        global_merger.update(file,data,flag,cnt)
        cnt += 1
    writer.write(players_data,'C:/Users/sidsu/Downloads/FPL_AI/Data/','Players.xlsx')

if __name__ == "__main__":
    main(sys.argv)