import csv
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import numpy as np
import PIL
from io import StringIO

class Graphs:

    def createAllLevelsGraph(testName, GMFCSLevel, previousAge, previousScore, currentAge, currentScore):
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
            pylab.xlabel('Age in Years')
            pylab.ylabel('Score')
            pylab.title(testName)
            pylab.show()

            buffer = StringIO.StringIO()
            canvas = pylab.get_current_fig_manager().canvas
            canvas.draw()
            pilImage = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
            pilImage.save(buffer, "PNG")
            pylab.close()
            return buffer.getvalue()

    def createPercentileGraph(testName, GMFCSLevel, previousAge, previousScore, currentAge, currentScore):
        with open("OnTrackWebsite/graphData/" + testName + "_level" + GMFCSLevel + ".csv") as data:
            csv_reader = csv.reader(data, delimiter=',')
            line_count = 0
            xAxis = []
            percentiles = {}
            for row in csv_reader:
                if line_count == 0:
                    for index in range(2, len(row)+1):
                        percentiles[int(row[index])] = []
                else:
                    xAxis.append(float(row[1]))
                    rownum = 2
                    keys = percentiles.keys()
                    for key in keys:
                        percentiles.get(key).append(row[rownum])
                        rownum += 1

                line_count += 1
            for percentile in percentiles:
                pylab.plot(xAxis, percentile)
            pylab.xlabel('Age in Years')
            pylab.ylabel('Score')
            pylab.title(testName)
            pylab.show()

            buffer = StringIO.StringIO()
            canvas = pylab.get_current_fig_manager().canvas
            canvas.draw()
            pilImage = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
            pilImage.save(buffer, "PNG")
            pylab.close()
            return buffer.getvalue()

Graphs.createAllLevelsGraph("CEDLpar", 1, [3, 4], 3.5, [4, 5], 4)