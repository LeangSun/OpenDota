import requests
import time
import os
import json


def read_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    else:
        return []


def write_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f)


def extend_json(filepath, new_data):
    data = read_json(filepath)
    data.extend(new_data)
    write_json(filepath, data)


def get_match(match_id):
    url = f"https://api.opendota.com/api/matches/{match_id}"
    response = requests.get(url)

    if response.status_code == 200:
        match_data = response.json()
        return match_data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def get_player_match(account_id):
    url = f"https://api.opendota.com/api/players/{account_id}/matches"

    response = requests.get(url)

    if response.status_code == 200:
        account_data = response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    return account_data


def get_player(account_id):
    url = f"https://api.opendota.com/api/players/{account_id}"
    response = requests.get(url)
    if response.status_code == 200:
        account_data = response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)  # 打印错误信息

    return account_data


def get_parsed_match(number_in_hundreds, less_than_match_id=None):
    # Construct url for API request
    url = f"https://api.opendota.com/api/parsedMatches"

    # Number of Parsed match needed (measured in hundreds)
    Parsed_Match_Number = range(number_in_hundreds)

    full_list_parsed_match = []
    for i in Parsed_Match_Number:
        query_params = {
            "less_than_match_id": less_than_match_id
        }
        response = requests.get(url, params=query_params)
        if response.status_code == 200:
            parsed_match = response.json()

            full_list_parsed_match.extend(parsed_match)
            less_than_match_id = int(parsed_match[-1]["match_id"])
            time.sleep(1.5)
            print("Succeed in getting 100 parsed match")

        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    parsed_match_index = [item["match_id"] for item in full_list_parsed_match]
    return parsed_match_index


# This function provides a list of parsed matches just ended, which can be considered as random sampling for matches.

def get_player_list(hundreds_of_parsed_match, filepath, less_than_match_id=None):
    parsed_match_index = get_parsed_match(hundreds_of_parsed_match, less_than_match_id)
    account_ids = []
    i = 0
    for index in parsed_match_index:
        match = None
        while match is None:
            match = get_match(index)
            time.sleep(1)
        i += 1
        players = match.get("players", [])
        for player in players:
            account_id = player.get("account_id")
            if account_id is not None and account_id not in account_ids:
                account_ids.append(account_id)
                extend_json(filepath, [account_id])
        print(
            f"{i} matches have been analyzed. The last match analyzed is {index}. {len(account_ids)} players have been "
            f"added")
    return account_ids


# get a list of unique players from recent parsed match. This sampling method is not random for players,
# as more active players are more likely to be selected

def test_players(account_id, timestamp):
    player_info = []
    rank = get_player(account_id)['rank_tier']
    time.sleep(1.5)
    player_info.append(rank)

    total_match_info = get_player_match(account_id)
    player_info.append(len(total_match_info))

    match_info = []
    parsed_match_info = []
    for match_data in total_match_info:
        if match_data['start_time'] > timestamp:
            match_info.append(match_data)
            if match_data['version'] is not None:
                parsed_match_info.append(match_data)
                # When "version" is not None, the match is parsed
        else:
            continue

    player_info.append(len(match_info))
    player_info.append(len(parsed_match_info))
    player_info.append(len(parsed_match_info) / len(match_info))
    time.sleep(1.5)
    print("Succeed in testing one player")

    return player_info

# This function provides information about the quality of a player's data.
# Information: Rank tier; Total number of matches; Number of matches before the timestamp;
# Number of parsed matches before the timestamp; Percentage of parsed matches before the time stamp
