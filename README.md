# OpenDota
The program retrieves players follow this procedure: 
  1. Retrieve recent parsed match, and then get players' account id. One call can get about 4.5 ids.
  2. Use two calls per player to get relevant information

Example.py is provided.

Firstly, use "get_player_list" to retrieve players from parsed match just ended. Since all matches' id are arranged chronologically on OpenDota, "less_than_match_id" parameter allows to start from a particular match. It helps maintain continuity in sampling. 

Here we use 

![image](https://github.com/LeangSun/OpenDota/assets/123008712/d38e3994-79e2-4557-8699-0ee8d2f2994b)


,which means, we want to retrieve players id from 100 parsed matches just ended before the match "7632820016"), and write the result in account_id.json. 100 calls provide 475 player id.

![image](https://github.com/LeangSun/OpenDota/assets/123008712/6983966b-1be1-459b-801a-10aab3d235ae)


To simplify the example, take the first ten players: 

![image](https://github.com/LeangSun/OpenDota/assets/123008712/e78bdbd1-2e5e-4caa-9600-06c30e519cbc)


In test_players(), "1609459200" indicates that we want to have information for each player after 2021/01/01. We have the following test_result:

![image](https://github.com/LeangSun/OpenDota/assets/123008712/3de8c031-e3e6-46e8-a0cb-2911ba6e53f4)

Take the first item as an example: [55, 3161, 3069, 266, 0.086673183447377]. For player 1032473510, his rank is 55 (which means Legend[5]). Total number of matches ever played is 3161. Number of matches after the timestamp is 3069. Number of parsed matches after the timestamp is 266, Percentage of parsed matches after the time stamp is 4.98%.

After simple adjustment, test_players can be modified to include more useful information. 





