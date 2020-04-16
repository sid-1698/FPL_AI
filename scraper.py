import requests
from bs4 import BeautifulSoup as bs 
import json
import pandas as pd
import re
import writer as utility

class fpl_scraper():
    json_data = {}
    players_data = pd.DataFrame()
    teams_data = pd.DataFrame()
    individual_data = pd.DataFrame()

    def __init__(self,api):
        self.api = api

    def get_data(self):
        response = requests.get(self.api)
        if response.status_code != 200:
            raise Exception("Response code was " + str(response.status_code))
        response = response.text
        fpl_scraper.json_data = json.loads(response)
        fpl_scraper.players_data = pd.DataFrame.from_records(fpl_scraper.json_data['elements'])
        fpl_scraper.teams_data = pd.DataFrame.from_records(fpl_scraper.json_data['teams'])
    
    def get_inidividual_data(self):
        response = requests.get(self.api)
        if response.status_code != 200:
            raise Exception("Response code was " + str(response.status_code))
        response = response.text
        fpl_scraper.json_data = json.loads(response)
        fpl_scraper.individual_data = pd.DataFrame.from_records(fpl_scraper.json_data['history'])


class fbref_scraper():
    soup = None
    table_data = []
    columns = []
    players_data = pd.DataFrame()
    teams_data = pd.DataFrame()
    individual_data = pd.DataFrame()

    def __init__(self,url):
        self.url = url
        self.fail = 0
    
    def get_soup(self):
        comm = re.compile("<!--|-->")
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception("Response code was " + str(response.status_code))
        response = response.text
        fbref_scraper.soup = bs(comm.sub("",response),'lxml')

    def get_table(self,id):
        try:
            table = fbref_scraper.soup.find('table',{'id': id})
            fbref_scraper.columns = []
            for item in table.find_all('th',{'class':'poptip'}):
                fbref_scraper.columns.append(item['data-stat'])
            fbref_scraper.table_data = table.find('tbody')
            fbref_scraper.table_data = fbref_scraper.table_data.find_all('tr')
        except:
            print("Unable to fetch information from ", self.url)      
            self.fail = 1
               
    def parse_data(self):
        data = pd.DataFrame(index=range(0,len(fbref_scraper.table_data)),columns=fbref_scraper.columns)
        ind = 0 

        if self.fail == 1:
            return pd.DataFrame(index=[0],columns=fbref_scraper.columns)

        for item in fbref_scraper.table_data:
            try:
                Class = item['class']
            except:
                Class = ' '
            if ((Class == ' ') | (Class[0] == 'non_qual')):
                if ((item.find('th').find('a') != None)):
                    data.loc[ind,item.find('th')['data-stat']] = item.find('th').find('a').text
                for x in item.find_all('td'):
                    data.loc[ind,x['data-stat']] = x.text
                try:
                    data.loc[ind,data.columns[-1]] = item.find_all('a')[-1]['href']
                except:
                    data.loc[ind,item.find('th')['data-stat']] = item.find('th').find('a').text
                ind += 1
        data.dropna(how='all',axis=0,inplace=True)
        return data
    
    def get_data(self):
        self.get_soup()
        self.get_table('stats_standard')
        fbref_scraper.players_data = self.parse_data()
        self.get_table('stats_standard_squads')
        fbref_scraper.teams_data = self.parse_data()

    def get_individual_data(self):
        self.get_soup()
        self.get_table('ks_matchlogs_all')
        fbref_scraper.individual_data = self.parse_data()


if __name__ == "__main__":
    pass