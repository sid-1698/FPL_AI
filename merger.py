import pandas as pd 
import numpy as np
import re 
import Levenshtein as lv
import warnings
import writer as utility
warnings.filterwarnings('ignore')

def get_similar(fpl_names,fbref_names):
    missing_names = []
    similar_names = {}
    for item in fpl_names:
        if item not in fbref_names:
            missing_names.append(item)
            similar_names[item] = ''
        else:
            similar_names[item] = item

    for item in missing_names:
        max_value = np.inf
        matching = ''
        for name in fbref_names: 
            if ((lv.distance(item,name) < max_value) & (name not in similar_names.values()) & (item[0] == name[0])):
                max_value = lv.distance(item,name)
                matching = name
                if lv.distance(item,name) == 0:
                    break
        if item == 'Spurs':
            matching = 'Tottenham'
        similar_names[item] = matching

    similar_names = {key:value for key,value in similar_names.items() if value != ''}
    return similar_names

def change_name(x,similar_names):
    if x in similar_names.values():
        return list(similar_names.keys())[list(similar_names.values()).index(x)]
    else:
        return np.nan

def overall_data(fpl,fbref):
    fpl['name'] = fpl['first_name'] + ' ' + fpl['second_name']
    
    fpl_names = fpl['name'].values.tolist()
    fbref_names = fbref['player'].values.tolist()

    similar_names = get_similar(fpl_names,fbref_names)
    fbref['player'] = fbref['player'].apply(lambda x : change_name(x,similar_names))

    overall_data = fbref.merge(fpl,how='inner',left_on = 'player',right_on = 'name').drop('player',axis=1)

    return overall_data

def teams_data(fpl,fbref):
    fpl_teams = fpl['name'].values.tolist()
    fbref_teams = fbref['squad'].values.tolist()

    similar_teams = get_similar(fpl_teams,fbref_teams)
    fbref['squad'] = fbref['squad'].apply(lambda x : change_name(x,similar_teams))
 
    merged_teams = fbref.merge(fpl,how='inner',left_on='squad',right_on='name').drop('squad',axis=1).sort_values('id')

    return merged_teams


def player_data(fpl,fbref):
    fbref = fbref[fbref['comp'] == 'Premier League']
    fbref['round'] = fbref['round'].apply(lambda x : int(re.findall(r'\d+',str(x))[0]))
    cols_to_merge = fpl.columns.difference(fbref.columns).tolist()
    cols_to_merge.append('round')

    merged_data = fbref.merge(fpl[cols_to_merge],how='outer',left_on='round',right_on='round').sort_values('round')

    return merged_data      


if __name__ == "__main__":
    pass
