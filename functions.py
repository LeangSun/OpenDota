import requests
import time


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


def get_parsed_match(number_in_hundreds):
    # Construct url for API request
    url = f"https://api.opendota.com/api/parsedMatches"

    # Number of Parsed match needed (measured in hundreds)
    Parsed_Match_Number = range(number_in_hundreds)

    # Get response
    less_than_match_id = None

    full_list_parsed_match = []
    for i in Parsed_Match_Number:
        query_params = {
            "less_than_match_id": less_than_match_id
        }
        response = requests.get(url, params=query_params)
        if response.status_code == 200:
            parsed_match = response.json()

            # Print and store parsed match
            full_list_parsed_match.extend(parsed_match)
            less_than_match_id = int(parsed_match[-1]["match_id"])

        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    parsed_match_index = [item["match_id"] for item in full_list_parsed_match]
    return parsed_match_index


# This function provides a list of parsed matches just ended, which can be considered as random sampling for matches.

def get_player_list(hundreds_of_parsed_match):
    parsed_match_index = get_parsed_match(1)

    matches = []
    for index in parsed_match_index:
        match = get_match(index)
        matches.append(match)

    account_ids = []
    for match in matches:
        players = match.get("players", [])
        time.sleep(2)
        for player in players:
            account_id = player.get("account_id")
            if account_id is not None:
                account_ids.append(account_id)

    unique_account_ids = list(set(account_ids))
    return unique_account_ids


# get a list of unique players from recent parsed match. This sampling method is not random for players,
# as more active players are more likely to be selected

def test_players(account_id, timestamp):
    player_info = []
    rank = get_player(account_id)['rank_tier']
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

    return player_info

# This function provides information about the quality of a player's data.
# Information: Rank tier; Total number of matches; Number of matches before the timestamp;
# Number of parsed matches before the timestamp; Percentage of parsed matches before the time stamp
