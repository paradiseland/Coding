"""
preprocess the PUBG data.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# read the source data.
AGG = pd.read_csv("./pubg-match-deaths/aggregate/agg_match_stats_0.csv")
DEATH = pd.read_csv("./pubg-match-deaths/deaths/kill_match_stats_final_0.csv")

# examine the data dimension & nan.
AGG.head()
AGG.info()
AGG.columns()
# ['date', 'game_size', 'match_id', 'match_mode', 'party_size',
# 'player_assists', 'player_dbno', 'player_dist_ride', 'player_dist_walk',
# 'player_dmg', 'player_kills', 'player_name', 'player_survive_time',
# 'team_id', 'team_placement']

# del data;match_mode;player_name
AGG['match_id'].value_counts()
AGG['player_name'].value_counts()
AGG['match_mode'].value_counts()

AGG.hist(bins=10, figsize=(20, 15))
plt.show()

AGG.head()
AGG.info()
AGG.columns()


# del na rows
AGG = AGG.dropna(how='any')

# select about 10,000 matches, including about 1000,000 data.
# that is 10,000 different match_id.

AGG_MatchIdValue = AGG['match_id'].value_counts()
index_gt99 = AGG_MatchIdValue.index[AGG_MatchIdValue > 99]
AGG_Selected = AGG[AGG['match_id'].isin(index_gt99)]
AGG_Selected.head()

# # processing the Nan
# AGG_Selected = AGG_Selected.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

# # drop the duplicate
# AGG_Selected = AGG_Selected.drop_duplicates(inplace=True)

# add a column of won or not
AGG_Selected['won'] = AGG_Selected['team_placement'] == 1

# add a column of drove or not
AGG_Selected['drove'] = AGG_Selected['player_dist_ride'] != 0
# delete the inactive players. 5412 deleted.
AGG_Selected = AGG_Selected.drop(
    AGG_Selected[AGG_Selected['player_dist_walk'] == 0].index)
# del the match mode
del AGG_Selected['match_mode']
AGG_Selected.to_csv('agg1.csv')

DEATH_MatchIdValue = DEATH['match_id'].value_counts()
indDEATH_gt99 = DEATH_MatchIdValue.index[DEATH_MatchIdValue >= 98]
DEATH_Selected = DEATH[DEATH['match_id'].isin(indDEATH_gt99)]
DEATH_Selected.head()
# processing the Nan
DEATH_Selected.dropna(how='any')

# drop the duplicate
# DEATH_Selected.drop_duplicates(inplace=True)


# processing the outliers. FOR THE DEATH!!! 642554 data
# for the kill distance > 1000m -> 100,000 dm
# add a column of kill distance.the distance or coordination unit is dm!
DEATH_Selected['kill_distance'] = np.sqrt((DEATH_Selected['killer_position_x']-DEATH_Selected['victim_position_x'])**2+(
    DEATH_Selected['killer_position_y']-DEATH_Selected['victim_position_y'])**2)
# 64
DEATH_Selected = DEATH_Selected.drop(
    DEATH_Selected[DEATH_Selected['kill_distance'] >= 100000].index)
# delete players who kill more than 30 ,than 638728 data.
killer_times = DEATH_Selected['killer_name'].value_counts()
DEATH_Selected = DEATH_Selected.drop(DEATH_Selected[DEATH_Selected['killer_name'].isin(
    killer_times[killer_times > 30].index)].index)
# generate the new data.6542 games.
DEATH_Selected.to_csv('death1.csv')


# REread the file.
AGG = pd.read_csv("agg1.csv")
DEATH = pd.read_csv("death1.csv")
