from functions import get_player_list, retrieve_player_info, test_players
account_ids = get_player_list(1, 'account_id.json', 442498217)


id_list = [1032473510, 405100511, 153202767, 912265313, 69537170, 362311368, 388300006, 258901728, 424640932, 160150038]
player_data = []
for id in id_list:
    data = retrieve_player_info(id)
    player_data.append(data)

test_result = []
for data in player_data:
    test = test_players(data, 1609459200)
    test_result.append(test)

print(test_result)
