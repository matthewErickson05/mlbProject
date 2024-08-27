import statsapi as mlb
import requests
import json
import pitchParser
import csv



games = mlb.schedule(start_date='04/01/2024',end_date='07/18/2024',team=143)

sortedGames = []
for game in games :
    if game["home_name"] == "Philadelphia Phillies" :
        if game["home_probable_pitcher"] == "Zack Wheeler" :
            sortedGames.append(game)
    if game["away_name"] == "Philadelphia Phillies" :
        if game["away_probable_pitcher"] == "Zack Wheeler" :
            sortedGames.append(game)

print(len(sortedGames))


final = list()
for game in sortedGames :
    #Creates a url with the play-by-play for the whole game
    url = "https://statsapi.mlb.com/api/v1/game/" + str(game["game_id"]) + "/playByPlay"
    # In this url there is a JSON split up into a list of all plays, within each entry of all plays is play events
    # which has the individual pitch data
    response = requests.get(url)

    if response.status_code == 200:
        # Step 2: Parse the JSON data
        data = response.json()

        # Step 3: Save the parsed data to a file
        with open("data.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
        
        isHome = game["home_name"] == "Philadelphia Phillies"
        output = pitchParser.getPitchingData("data.json", isHome,554430)
        for value in output : 
            final.append(value)

    else:
        print(f"Failed to fetch data. HTTP Status code: {response.status_code}")

print(len(final))

#writes the csv file with all of the pitching data
with open("zackWheeler2024Pitches.csv", 'w') as pitches :
    writer = csv.writer(pitches)
    for row in final :
        writer.writerow(row)
