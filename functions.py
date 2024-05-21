import json
import os
import sys
import time
import requests
import psutil


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


def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss


def get_match(match_id):
    url = f"https://api.opendota.com/api/matches/{match_id}"
    query_params = {
        "api_key": '42d8d1f9-cdb4-49e3-805a-9738c5bfc5e8'
    }
    response = requests.get(url, params=query_params)

    if response.status_code == 200:
        match_data = response.json()
        return match_data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def get_player_match(account_id, project=None):
    url = f"https://api.opendota.com/api/players/{account_id}/matches"
    query_params = {
        "project": str(project),
        "api_key": '42d8d1f9-cdb4-49e3-805a-9738c5bfc5e8'
    }
    response = requests.get(url, params=query_params)

    if response.status_code == 200:
        account_data = response.json()
        return account_data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def get_player_recent_match(account_id):
    url = f"https://api.opendota.com/api/players/{account_id}/recentMatches"
    query_params = {
        "api_key": '42d8d1f9-cdb4-49e3-805a-9738c5bfc5e8'
    }
    response = requests.get(url, params=query_params)

    if response.status_code == 200:
        account_data = response.json()
        return account_data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def get_player(account_id):
    url = f"https://api.opendota.com/api/players/{account_id}"
    query_params = {
        "api_key": '42d8d1f9-cdb4-49e3-805a-9738c5bfc5e8'
    }
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        account_data = response.json()
        return account_data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def get_public_match(number_in_hundreds, less_than_match_id=None):
    url = f"https://api.opendota.com/api/publicMatches"

    public_match_number = range(number_in_hundreds)

    full_list_public_match = []
    for i in public_match_number:
        query_params = {
            "less_than_match_id": less_than_match_id,
            "api_key": '42d8d1f9-cdb4-49e3-805a-9738c5bfc5e8'
        }
        response = requests.get(url, params=query_params)
        if response.status_code == 200:
            public_match = response.json()

            full_list_public_match.extend(public_match)
            less_than_match_id = int(public_match[-1]["match_id"])
            time.sleep(0.05)
            print("Succeed in getting 100 public match")

        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            i = i - 1
    return full_list_public_match


def get_parsed_match(number_in_hundreds, less_than_match_id=None):
    # Construct url for API request
    url = f"https://api.opendota.com/api/parsedMatches"

    # Number of Parsed match needed (measured in hundreds)
    Parsed_Match_Number = range(number_in_hundreds)

    full_list_parsed_match = []
    for i in Parsed_Match_Number:
        query_params = {
            "less_than_match_id": less_than_match_id,
            "api_key": '42d8d1f9-cdb4-49e3-805a-9738c5bfc5e8'
        }
        response = requests.get(url, params=query_params)
        if response.status_code == 200:
            parsed_match = response.json()

            full_list_parsed_match.extend(parsed_match)
            less_than_match_id = int(parsed_match[-1]["match_id"])
            time.sleep(0.05)
            print("Succeed in getting 100 parsed match")

        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    parsed_match_index = [item["match_id"] for item in full_list_parsed_match]
    return parsed_match_index


# This function provides a list of parsed matches just ended, which can be considered as random sampling for matches.

def get_player_list(match_index, filepath, less_than_match_id=99999999999999999):
    account_ids = list(read_json(filepath))
    i = 0
    for index in match_index:
        if index < less_than_match_id:
            match = None
            while match is None:
                match = get_match(index)
                time.sleep(0.05)
            i += 1
            players = match.get("players", [])
            for player in players:
                account_id = player.get("account_id")
                if account_id is not None and account_id not in account_ids:
                    account_ids.append(account_id)
                    write_json(filepath, [account_ids])
            print(
                f"{i} matches have been analyzed. The last match analyzed is {index}. {len(account_ids)} players have been "
                f"added")
    return account_ids


# get a list of unique players from recent parsed match. This sampling method is not random for players,
# as more active players are more likely to be selected

def retrieve_player_info(account_id):
    player_info = []
    account_info = get_player(account_id)
    time.sleep(0.05)
    player_info.append(account_info)

    total_match_info = get_player_match(account_id)
    time.sleep(0.05)
    player_info.append(total_match_info)

    recent_match_info = get_player_recent_match(account_id)
    time.sleep(0.05)
    player_info.append(recent_match_info)

    if len(player_info) == 3:
        print(f"Succeed in retrieving {account_id}")
    else:
        print("Failure! The last account_id tried is {account_id}")
        sys.exit()

    return player_info


def test_players(info, timestamp):
    player_info = []
    rank = info[0]['rank_tier']
    time.sleep(0.05)
    player_info.append(rank)
    player_info.append(len(info[1]))

    match_info = []
    parsed_match_info = []
    for match_data in info[1]:
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
    time.sleep(0.05)
    print(f"Succeed in analyzing player {info[0]['profile']['account_id']}")

    return player_info


# This function provides information about the quality of a player's data.
# Information: Rank tier; Total number of matches; Number of matches before the timestamp;
# Number of parsed matches before the timestamp; Percentage of parsed matches before the time stamp

def search_id(time_target):  # 这个time应该是某日凌晨一点的timestamp
    id_1 = 7288601836
    id_2 = id_1 + (time_target - 1692262536) * 100
    left_id = min(id_1, id_2)
    right_id = max(id_1, id_2)
    id_hat = (left_id + right_id) / 2

    result = get_public_match(1, less_than_match_id=id_hat)
    start_time_hat = result[0]["start_time"]
    time.sleep(0.05)

    while abs(start_time_hat - time_target) > 60:
        if start_time_hat > time_target:
            right_id = id_hat
            id_hat = round((left_id + right_id) / 2)
            result = get_public_match(1, less_than_match_id=id_hat)
            time.sleep(0.05)
            start_time_hat = result[0]["start_time"]

        else:
            left_id = id_hat
            id_hat = round((left_id + right_id) / 2)
            result = get_public_match(1, less_than_match_id=id_hat)
            time.sleep(0.05)
            start_time_hat = result[0]["start_time"]

    return id_hat


def search_hour(filepath, time_start, hours, number_of_match=1):
    match_sample = []
    for i in range(0, hours):
        hour_match = get_public_match(number_of_match, less_than_match_id=search_id(time_start))
        match_sample.append(hour_match)
        extend_json(filepath, hour_match)
        print(f"{number_of_match} hundred match data saved")
        time_start += 3600
    return match_sample


#这个地方多看一下


def get_match_id(match_list_day):
    match_index = []
    for match in match_list_day:
        match_index.append(match['match_id'])
    return match_index
