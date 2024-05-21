from functions import get_player_list, read_json
date = "8_19"
match_id = read_json(
    fr"C:\Users\Sunle\Desktop\PycharmProjects\pythonProject\OpenDota\Main\Data\First_trial\{date}_matchid_first.json")
player_list = get_player_list(match_id,
                              fr"C:\Users\Sunle\Desktop\PycharmProjects\pythonProject\OpenDota\Main\Data\First_trial\{date}_playerid_first.json",
                              7293440402)
