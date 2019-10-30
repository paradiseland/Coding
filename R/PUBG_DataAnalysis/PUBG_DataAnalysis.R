pubg_data_aggregate <- read.csv("D:/PUBG_data/pubg-match-deaths/aggregate/agg_match_stats_0.csv")
pubg_data_death <- read.csv("D:/PUBG_data/pubg-match-deaths/deaths/kill_match_stats_final_0.csv")
# show features' name
colnames(pubg_data_aggregate)
colnames(pubg_data_death)

pubg_data_aggregate$player_name <- as.character(pubg_data_aggregate$player_name)

