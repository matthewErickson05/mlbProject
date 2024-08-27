import json
import random

#Open json file


def getPitchingData(jsonName, isHome, pitcherID) :
    with open(jsonName) as f:
        data = json.load(f)

        battersFaced = 0
        pitchZones = dict()
        postOnFirst = None
        postOnSecond = None
        postOnThird = None
        for x in range(1,15) :
            pitchZones[x] = 0

        pitchTypes = dict()
        isTop = True
        homeScore = 0
        awayScore = 0
        gameDiff = 0
        pitches = 0
        outs = 0

        accumulate = list()
        #iterates through every "play", which is an at-bat
        for play in data['allPlays'] :
            if play["about"]["isTopInning"] != isTop :
                postOnFirst = None
                postOnSecond = None
                postOnThird = None
                isTop = not isTop
                outs = 0
            #if Zack Wheeler is pitching
            if play['matchup']['pitcher']['id'] ==  pitcherID:
                battersFaced += 1
                #if the play resulted in an out

                batterid = play["matchup"]["batter"]['id']
                batterLefty = play['matchup']['batSide']['code'] == "L"
                
                ratingFB = round(random.uniform(4.9, 5.1), 2)
                xCoordsAB = []
                zCoordsAB = []
                normSpeedsAB = []
                ratingLR = round(random.uniform(1.9, 2.1), 2)
                ratingUD = round(random.uniform(1.9, 2.1), 2)
                balls = 0
                strikes = 0
                #Takes each pitch in an at-bat
                for event in play["playEvents"] :
                    if event['isPitch'] :

                        #categorizes the zone
                        try :
                            zone = event["pitchData"]["zone"]
                            pitchZones[zone] += 1
                        except :
                            break

                        speed = event["pitchData"]["startSpeed"]
                        spinRate = event["pitchData"]["breaks"]["spinRate"]
                        typePitch = event["details"]["type"]['description']


                        ##This is where I'm going to store the pitch
                        pitch = (int(pitches), postOnFirst, postOnSecond, postOnThird, gameDiff, batterid, batterLefty, balls, strikes, outs, ratingLR, ratingUD, ratingFB, zone, speed, spinRate, typePitch)
                        accumulate.append(pitch)

                        #Tallies the types of pitches thrown for the whole game
                        try :
                            pitchTypes[event["details"]["type"]['description']] += 1
                        except :
                            pitchTypes[event["details"]['type']['description']] = 1

                        #Tallies the strikes and balls
                        if event['details']['isBall'] :
                            balls += 1
                            call = "ball"
                        elif event['details']['isStrike'] :
                            strikes += 1
                            call = "strike"
                        elif event['details']['isInPlay'] :
                            strikes += 1 #In actual implementation idk if I will keep this.
                            call = "inPlay"
                            
                        pitches += 1

                        #Creates the ratings for dimensions, i.e. how much the pitcher has worked the batter 
                        # (close to 1 means the pitcher has not worked the batter at all, maybe early in the count)
                        # numbers are initialized between 4.9 and 5.1 for each at bat, go from 0.0 to 10
                        #First we do left to right:
                        breakHorizontal = event["pitchData"]["breaks"]["breakHorizontal"]
                        fopXCoor = event["pitchData"]["coordinates"]["pX"]
                        ratingLR = round(random.uniform(1.95, 2.05), 2)
                        #Takes the weighted average of the numbers where the more recent numbers get higher weights
                        if abs(fopXCoor) < 1.6 :
                            xCoordsAB.append(fopXCoor)
                            weights = list(range(1, len(xCoordsAB) + 1))
                            weighted_sum = sum(number * weight for number, weight in zip(xCoordsAB, weights))
                            avgX = weighted_sum / sum(weights)
                            ratingLR += avgX
                        ratingLR = round(ratingLR, 4)
                        #Next we do up and down
                        breakVertical = event["pitchData"]["breaks"]["breakVerticalInduced"]
                        centerStrikeZone = event["pitchData"]["strikeZoneTop"] - event["pitchData"]["strikeZoneBottom"]
                        fopZCoor = event["pitchData"]["coordinates"]["pZ"]
                        fopZCoor = fopZCoor - centerStrikeZone
                        ratingUD = round(random.uniform(1.95, 2.05), 2)
                        if abs(fopZCoor) < 2.5 :
                            zCoordsAB.append(fopZCoor)
                            weights = list(range(1, len(zCoordsAB) + 1))
                            weighted_sum = sum(number * weight for number, weight in zip(zCoordsAB, weights))
                            avgZ = weighted_sum / sum(weights)
                            ratingUD += avgZ
                        ratingUD = round(ratingUD, 4)
                        #Next we do front and back (speed)
                        normSpeed = speed / 17.3
                        normSpeed = normSpeed - 5
                        ratingFB = round(random.uniform(4.9, 5.1), 2)
                        normSpeedsAB.append(normSpeed)
                        weights = list(range(1, len(normSpeedsAB) + 1))
                        weighted_sum = sum(number * weight for number, weight in zip(normSpeedsAB, weights))
                        avgSpeed = weighted_sum / sum(weights)
                        ratingFB += avgSpeed
                        ratingFB = round(ratingFB, 4)

                        
                    else :
                        try :
                            if play["isBaseRunningPlay"] :
                                break
                        except :
                            pass
                    
                    

                #Updates the score between each at-bat 
                homeScore = play["result"]["homeScore"]
                awayScore = play["result"]["awayScore"]
                gameDiff = homeScore - awayScore
                if (isHome) :
                    gameDiff = -1 * gameDiff
                
                if play['result']['isOut'] :
                    outs += 1

                #Updates the bases between each at-bat
                try:
                    postOnFirst = play["matchup"]['postOnFirst']['id']
                except :
                    postOnFirst = None
                try: 
                    postOnSecond = play['matchup']['postOnSecond']['id']
                except :
                    postOnSecond = None
                try: 
                    postOnThird = play['matchup']['postOnThird']['id']
                except :
                    postOnThird = None
            #Updates the score between each inning
            homeScore = play["result"]["homeScore"]
            awayScore = play["result"]["awayScore"]
            gameDiff = homeScore - awayScore
            if (not isHome) :
                gameDiff = -1 * gameDiff
                        


        # print("\nZONES")
        # zones = pitchZones.keys()
        # for key in zones :
        #     print("Zone " + str(key) + ": " + str(pitchZones[key]))

        # print("\nTYPES")
        # sumtypes = 0
        # types = pitchTypes.keys()
        # for key in types :
        #     print(str(key) + ": " + str(pitchTypes[key]))
        #     sumtypes += pitchTypes[key]

        # print(sumtypes)
        # print(pitches)

        for thing in accumulate :
            print(str(thing))
        
        return accumulate
