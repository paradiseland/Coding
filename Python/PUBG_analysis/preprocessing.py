"""
preprocess the PUBG data.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("zz")
print("gg")




AGG = pd.read_csv("./pubg-match-deaths/aggregate/agg_match_stats_0.csv")

DEATH = pd.read_csv("./pubg-match-deaths/deaths/kill_match_stats_final_0.csv")

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

AGG_grouped = AGG.groupby(['match_id'])

# delete the match which has palyers less than 80.
less80 = []
for index, value in AGG['match_id'].value_counts().items():
    if value < 80:
        less80.append(index)


AGG_Filter80 = AGG[AGG['match_id'].isin(less80)]
setless80 = set(AGG_Filter80.index)
set_all = set(range(len(AGG)))
set_select = list(set_all - setless80)
AGG_Selected = AGG.loc[set_select]

# del na rows
AGG.dropna(how='any')

AGG.colu

AGG.columns
