from functions import search_hour
from functions import write_json, read_json, get_match_id

date = "8_19"

result = search_hour(
    fr"C:\Users\Sunle\Desktop\PycharmProjects\pythonProject\OpenDota\Main\Data\First_trial\{date}_matchid_first.json",
    1692486000, 4, 30)

data = read_json(fr"C:\Users\Sunle\Desktop\PycharmProjects\pythonProject\OpenDota\Main\Data\First_trial\{date}_matchid_first.json")
match_id = sorted(get_match_id(data), reverse=True)
write_json(fr"C:\Users\Sunle\Desktop\PycharmProjects\pythonProject\OpenDota\Main\Data\First_trial\{date}_matchid_first.json",
           match_id)

print(len(match_id))