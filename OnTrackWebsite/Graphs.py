import csv
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import numpy as np
import PIL
from io import BytesIO
import base64
from OnTrackWebsite.CheckProgress import CheckProgress

class Graphs:

    percentileChoices = [3, 50, 80]
    levelChoices = ["Level I", "Level II", "Level III", "Level IV", "Level V"]

    def getAgeInYears(ageArray):
        return ageArray[0] + ageArray[1] / 12

    def createAllLevelsGraph(testName, GMFCSLevel, previousAge, previousScore, currentAge, currentScore, levelChoices):
        with open("OnTrackWebsite/graphData/" + testName + "_all_levels.csv") as data:
            csv_reader = csv.reader(data, delimiter=',')
            line_count = 0
            xAxis = []
            levels = [[], [], [], [], []]
            for row in csv_reader:
                if line_count != 0:
                    xAxis.append(float(row[1]))
                    for level in range(2,7):
                        levels[level - 2].append(float(row[level]))

                line_count += 1
            for level in levels:
                pylab.plot(xAxis, level)
            previousAgeInYears = Graphs.getAgeInYears(previousAge)
            currentAgeInYears = Graphs.getAgeInYears(currentAge)
            pylab.plot([previousAgeInYears, currentAgeInYears], [previousScore, currentScore])
            pylab.xlabel('Age in Years')
            pylab.ylabel('Score')
            pylab.title(testName)
            levelChoices.append("Your result")
            pylab.legend(levelChoices)
            #pylab.show()

            buffer = BytesIO()
            canvas = pylab.get_current_fig_manager().canvas
            canvas.draw()
            pilImage = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
            pilImage.save(buffer, "PNG")
            pylab.close()
            img_str = base64.b64encode(buffer.getvalue())
            return img_str

    def createPercentileGraph(testName, GMFCSLevelInt, previousAge, previousScore, currentAge, currentScore, percentileChoices=None):
        with open("OnTrackWebsite/graphData/" + testName + "_level" + str(GMFCSLevelInt) + ".csv") as data:
            csv_reader = csv.reader(data, delimiter=',')
            line_count = 0
            xAxis = []
            percentiles = {}
            for row in csv_reader:
                if line_count == 0:
                    for index in range(2, len(row)):
                        percentiles[int(row[index])] = []
                else:
                    xAxis.append(float(row[1]))
                    rownum = 2
                    keys = percentiles.keys()
                    for key in keys:
                        percentiles.get(key).append(float(row[rownum]))
                        rownum += 1

                line_count += 1
            keys = percentiles.keys()
            if(not percentileChoices == None):
                keys = list(filter(lambda x: x in percentileChoices, keys))
            for key in keys:
                pylab.plot(xAxis, percentiles.get(key))
            previousAgeInYears = Graphs.getAgeInYears(previousAge)
            currentAgeInYears = Graphs.getAgeInYears(currentAge)
            pylab.plot([previousAgeInYears, currentAgeInYears], [previousScore, currentScore])
            pylab.xlabel('Age in Years')
            pylab.ylabel('Score')
            stringKeys = []
            for key in keys:
                stringKeys.append(str(key))
            stringKeys.append("Your result")
            pylab.title(testName)
            pylab.legend(stringKeys)
            #pylab.show()

            buffer = BytesIO()
            canvas = pylab.get_current_fig_manager().canvas
            canvas.draw()
            pilImage = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
            pilImage.save(buffer, "PNG")
            pylab.close()
            img_str = base64.b64encode(buffer.getvalue())
            return img_str

    def getAllGraphs(GMFCSLevelInt, age, scores):
        result = {}
        testNamesForSheets = ["ECAB", "SMWT", "SAROMM", "CEDLpar", "CEDLsc", "EASE", "FSA", "HEALTH", "GMFM"]
        testNumbers = range(len(testNamesForSheets))
        if(scores[1][0] == None):
            del testNumbers[1]
        for testIndex in testNumbers:
            result[testNamesForSheets[testIndex]] = [Graphs.createAllLevelsGraph(testNamesForSheets[testIndex], GMFCSLevelInt, age[0], scores[testIndex][0], age[1], scores[testIndex][1], Graphs.levelChoices), Graphs.createPercentileGraph(testNamesForSheets[testIndex], GMFCSLevelInt, age[0], scores[testIndex][0], age[1], scores[testIndex][1], Graphs.percentileChoices)]
        return result


#Graphs.createAllLevelsGraph("CEDLpar", 1, [3, 4], 3.5, [4, 5], 4, ["Level I", "Level II", "Level III", "Level IV", "Level V"])
#Graphs.createPercentileGraph("CEDLpar", 1, [3, 4], 3.5, [4, 5], 4, [3, 50, 80])
