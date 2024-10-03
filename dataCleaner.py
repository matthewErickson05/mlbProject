import statsapi as mlb
import csv

#This file is meant to clean and normalize the data and return a new csv which will be used in the model
def cleanData(csvFile) :
    #Create readers and writers for the new and old data
    with open("clean_data.csv", 'w', newline='') as clean :
        with open(csvFile, 'r') as data :
            writer = csv.writer(clean)
            reader = csv.reader(data)
            writer.writerow(["PitchCount", "RunnersOn", "ScoreDiff", "BattingAVG", "isBatterRighty", "balls", "strikes", "outs", "ratingLR", "ratingUD", "ratingFB"])

            readThis = True
            batters = dict()
            count = 0
            for line in reader :
                # if count > 10 :
                #     break
                if readThis :
                    edited = list()
                    edited.append(float(line[0]))

                    #First we need to handle runners on base, with zero runners on going to 0, and then the sum of runner values:
                    #1st base: 1, 2nd base: 2, 3rd base: 3
                    basesSum = 0.0
                    print(type(line[1]))
                    if line[1] != '':
                        basesSum += 1.0
                    if line[2] != '' :
                        basesSum += 2.0
                    if line[3] != '' :
                        basesSum += 3.0
                    edited.append(basesSum)

                    edited.append(float(line[4]))

                    #Next we need to input the batter data
                    try:
                        ops = batters[line[5]]
                    except :
                        batterData = mlb.player_stat_data(line[5], 'hitting', 'season')
                        batters[line[5]] = float(batterData["stats"][0]['stats']['ops'])
                        ops = batters[line[5]]
                    
                    edited.append(ops)

                    if line[6] == "True" :
                        edited.append(0.0)
                    else :
                        edited.append(1.0)
                    
                    for x in range(7,13) :
                        edited.append(float(line[x]))
                    
                    print(edited)
                    writer.writerow(edited)
                    # count += 1

                readThis = not readThis

def createLabels(csvFile) :
    with open("labels.csv", 'w', newline='') as labels :
        with open(csvFile, 'r') as data :
            writer = csv.writer(labels)
            reader = csv.reader(data)

            readThis = True
            for line in reader :
                if readThis :
                    thing =  list()
                    thing.append(line[16])
                    #thing.append(line[13])
                    writer.writerow(thing)
                readThis = not readThis
                    

cleanData('zackWheeler2024Pitches.csv')
#createLabels('zackWheeler2024Pitches.csv')