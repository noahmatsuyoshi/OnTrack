import numpy
import xlrd
import os 
import math

# Represents a progress value for a particular test
# Progress should be an array of char values: 'l', 'a', or 'm'
class ProgressValue:

    def __init__(self, progress):
        self.isRange = len(progress) != 1
        self.progress = progress
    
    def __str__(self):
        return str(self.progress)

# Represents a progress value for a particular test
# If endRange is blank, the range goes to 100, and if startRange is blank, the range starts at 0
# If a range is not given, value will be assigned to startRange and endRange
class PercentileValue:

    def __init__(self, value=None, startRange=0, endRange=100):
        if(value == None):
            self.isRange = True
            self.startRange = startRange
            self.endRange = endRange
        else:
            self.isRange = False
            self.startRange = value
            self.endRange = value
    
    def __str__(self):
        return str([self.startRange, self.endRange])


class CheckProgress:

    # Static, Global variables
    file_name = "OnTrackWebsite/data.xlsx"
    testNamesForSheets = ["ECAB", "SMWT", "SAROMM", "CEDLpar", "CEDLsc", "EASE", "FSA", "HEALTH", "GMFM"]
    romanNumeralMap = {
        "I": 1,
        "II": 2,
        "III": 3,
        "IV": 4,
        "V": 5
    }

    # Map of test name to row number (zero-based) of centile change sheets table 
    mapForDifferenceSheets = {
        "ECAB": 5, 
        "SMWT": 6, 
        "SAROMM": 7, 
        "CEDLpar": 0, 
        "CEDLsc": 1, 
        "EASE": 2, 
        "FSA": 3, 
        "HEALTH": 4, 
        "GMFM": 8
    }
    mapForOutput = {
        "ECAB": 0, 
        "SMWT": 3, 
        "SAROMM": 2, 
        "CEDLpar": 6, 
        "CEDLsc": 7, 
        "EASE": 4, 
        "FSA": 1, 
        "HEALTH": 5, 
        "GMFM": 8
    }

    #testNames = ["ECAB"] #For testing run only ECAB
    percentileRow = 1
    centileChangeColumnOffset = 1
    centileChangeRowOffset = 1
    lowerCentileChangeTableName = "TenPercentValuesCentileChangeSc"
    upperCentileChangeTableName = "NineyPercentValuesCentileChange"

    numTests = len(testNamesForSheets)

    workbook = xlrd.open_workbook(file_name)
    lowerCentileChangeSheet = workbook.sheet_by_name(lowerCentileChangeTableName)
    upperCentileChangeSheet = workbook.sheet_by_name(upperCentileChangeTableName)



    # Inputs (Assume inputs are valid at this point, will handle validation in web form)
    name = "Bobby Boy"
    GMFCSLevel = "I"
    age = [[3, 5], [4, 3]] # [[past year, past month], [current year, current month]]
    # Assign scores in this order: "ECAB", "SMWT", "SAROMM", "CEDLpar", "CEDLsc", "EASE", "FSA", "HEALTH", "GMFM"
    # With first element being past score and second current
    scores = [[80, 95], [1175, 2000], [1, 0.3], [55, 70], [35, 50], [3, 4], [2, 3], [1, 5], [22, 100]]
    

    def performCalculation(GMFCSLevel, age, scores):
        GMFCSLevelInt = CheckProgress.romanNumeralMap.get(GMFCSLevel)
        centileChange = [CheckProgress.lowerCentileChangeSheet.col_slice(CheckProgress.centileChangeColumnOffset+GMFCSLevelInt-1, CheckProgress.centileChangeRowOffset, CheckProgress.centileChangeRowOffset+CheckProgress.numTests), CheckProgress.upperCentileChangeSheet.col_slice(CheckProgress.centileChangeColumnOffset+GMFCSLevelInt-1, CheckProgress.centileChangeRowOffset, CheckProgress.centileChangeRowOffset+CheckProgress.numTests)]

        percentiles = CheckProgress.getPercentiles(GMFCSLevel, age, scores, centileChange, GMFCSLevelInt <= 3) 
        progress = CheckProgress.getProgress(GMFCSLevel, percentiles, centileChange, GMFCSLevelInt <= 3) 

        # Reorder to match output in excel
        scores = CheckProgress.changeArrayOrder(scores, CheckProgress.mapForOutput)
        progress = CheckProgress.changeArrayOrder(progress, CheckProgress.mapForOutput)
        percentiles = CheckProgress.changeArrayOrder(percentiles, CheckProgress.mapForOutput)

        return {"progress": progress, "percentiles": percentiles, "scores": scores}

    # Takes age as input and returns row number to use for all tables
    def getRowNumFromAge(age):
        monthRow = math.floor(age[1]/3)
        return age[0]*4+monthRow-6

    def changeArrayOrder(array, transferMap):
        result = array.copy()
        for testIndex in range(CheckProgress.numTests):
            result[transferMap.get(CheckProgress.testNamesForSheets[testIndex])] = array[testIndex]
        return result


    # Looks through an array of cells to find start and end indices of the percent table
    def findStartAndEndCol(cells):
        startAndEnd = []
        for index in range(len(cells)):
            if(cells[index].ctype == 2 and len(startAndEnd) == 0):
                startAndEnd.append(index)
            elif(cells[index].ctype != 2 and len(startAndEnd) == 1):
                startAndEnd.append(index)
                return startAndEnd

    # Gets all percentile values for all tests for both current and past checkups
    def getPercentiles(GMFCSLevel, age, scores, centileChange, smwt):
        percentiles = []
        testNumbers = range(CheckProgress.numTests)
        if(not smwt):
            del testNumbers[1]
        for testIndex in testNumbers:
            sheetName = CheckProgress.testNamesForSheets[testIndex]+"_Level_"+GMFCSLevel
            sheet = CheckProgress.workbook.sheet_by_name(sheetName)
            
            percentileOfThisTest = []
            for timeIndex in range(2):
                row = CheckProgress.getRowNumFromAge(age[timeIndex])
                selectedRow = sheet.row(row)
                [percentileStartCol, percentileEndCol] = CheckProgress.findStartAndEndCol(selectedRow)
                selectedRow = sheet.row_slice(row, percentileStartCol, percentileEndCol)
                closestScoreIndexStartRange = -1
                closestScoreIndexEndRange = -1

                # Find score cells that match
                thisScore = scores[testIndex][timeIndex]
                for cellIndex in range(len(selectedRow)):
                    currentCellValue = float(selectedRow[cellIndex].value)

                    if(currentCellValue > thisScore):
                        if(closestScoreIndexStartRange == -1):
                            closestScoreIndexStartRange = cellIndex-1
                        closestScoreIndexEndRange = cellIndex-1
                        break
                    elif(currentCellValue == thisScore):
                        if(closestScoreIndexStartRange == -1):
                            closestScoreIndexStartRange = cellIndex
                        closestScoreIndexEndRange = cellIndex
                
                # Check for range conditions
                if(cellIndex == len(selectedRow)-1):
                    value = float(sheet.cell(CheckProgress.percentileRow, len(selectedRow)-1+percentileStartCol).value)
                    percentileOfThisTime = PercentileValue(startRange=value)
                elif(cellIndex == 0):
                    value = float(sheet.cell(CheckProgress.percentileRow, percentileStartCol).value)
                    percentileOfThisTime = PercentileValue(endRange=value)
                elif(closestScoreIndexStartRange == closestScoreIndexEndRange):
                    value = float(sheet.cell(CheckProgress.percentileRow, closestScoreIndexStartRange+percentileStartCol).value)
                    percentileOfThisTime = PercentileValue(value=value)
                else:
                    value1 = float(sheet.cell(CheckProgress.percentileRow, closestScoreIndexStartRange+percentileStartCol).value)
                    value2 = float(sheet.cell(CheckProgress.percentileRow, closestScoreIndexEndRange+percentileStartCol).value)
                    percentileOfThisTime = PercentileValue(startRange=value1, endRange=value2)
                percentileOfThisTest.append(percentileOfThisTime)
                
            percentiles.append(percentileOfThisTest)
        return percentiles

    # Return 2D array, first dimension corresponds to tests and second contains potential range of "less, as, or greater"
    # Array is ordered the same as the testNamesForSheets
    def getProgress(GMFCSLevel, percentiles, centileChange, smwt):
        progress = []
        testNumbers = range(CheckProgress.numTests)
        if(not smwt):
            del testNumbers[1]
        for testIndex in testNumbers:

            # Get potential range of difference
            pastPercentile = percentiles[testIndex][0]
            currentPercentile = percentiles[testIndex][1]
            maxDifference = currentPercentile.endRange - pastPercentile.startRange
            minDifference = currentPercentile.startRange - pastPercentile.endRange
            difference = [minDifference, maxDifference]
            print(str(pastPercentile) + ", " + str(currentPercentile))
            centileChangeRow = CheckProgress.mapForDifferenceSheets.get(CheckProgress.testNamesForSheets[testIndex])

            thisProgress = []
            # First check if change is under lower bound, then in between bounds, then above upper bound
            if(difference[0] < centileChange[0][centileChangeRow].value):
                thisProgress.append('*')
            else:
                thisProgress.append('')
            if(difference[1] > centileChange[0][centileChangeRow].value and difference[0] < centileChange[1][centileChangeRow].value):
                thisProgress.append('*')
            else:
                thisProgress.append('')
            if(difference[1] > centileChange[1][centileChangeRow].value):
                thisProgress.append('*')
            else:
                thisProgress.append('')

            if(testIndex == 2 or testIndex == 7):
                thisProgress.reverse()
            progress.append(thisProgress)
        
        return progress



