import numpy
from fpdf import FPDF
import xlrd
import os 

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

# Inputs (Assume inputs are valid at this point, will handle validation in web form)
GMFCSLevel = "III"
age = [[3, 5], [4, 3]] # [[past year, past month], [current year, current month]]
# Assign scores in this order: "ECAB", "SMWT", "SAROMM", "CEDLpar", "CEDLsc", "EASE", "FSA", "HEALTH", "GMFM"
# With first element being past score and second current
scores = [[25, 30], [220, 400], [1, 2], [55, 70], [35, 50], [3, 4], [2, 3], [3, 1], [22, 100]]


# Static, Global variables
file_name = "data.xlsx"
testNamesForSheets = ["ECAB", "SMWT", "SAROMM", "CEDLpar", "CEDLsc", "EASE", "FSA", "HEALTH", "GMFM"]
romanNumeralMap = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5
}
GMFCSLevelInt = romanNumeralMap.get(GMFCSLevel)
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
centileChange = [lowerCentileChangeSheet.col_slice(centileChangeColumnOffset+GMFCSLevelInt-1, centileChangeRowOffset, centileChangeRowOffset+numTests), upperCentileChangeSheet.col_slice(centileChangeColumnOffset+GMFCSLevelInt-1, centileChangeRowOffset, centileChangeRowOffset+numTests)]

# Takes age as input and returns row number to use for all tables
def getRowNumFromAge(age):
    monthRow = round(age[1]/3)
    return age[0]*4+monthRow-6

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
def getPerentiles(GMFCSLevel, age, scores):
    percentiles = []
    for testIndex in range(numTests):
        sheetName = testNamesForSheets[testIndex]+"_Level_"+GMFCSLevel
        sheet = workbook.sheet_by_name(sheetName)
        
        percentileOfThisTest = []
        for timeIndex in range(2):
            row = getRowNumFromAge(age[timeIndex])
            selectedRow = sheet.row(row)
            [percentileStartCol, percentileEndCol] = findStartAndEndCol(selectedRow)
            selectedRow = sheet.row_slice(row, percentileStartCol, percentileEndCol)
            closestScoreIndexStartRange = -1
            closestScoreIndexEndRange = -1
            for cellIndex in range(len(selectedRow)):
                currentCellValue = float(selectedRow[cellIndex].value)
                thisScore = scores[testIndex][timeIndex]
                
                if(currentCellValue > thisScore):
                    closestScoreIndexStartRange = cellIndex-1
                    closestScoreIndexEndRange = cellIndex-1
                    break
                elif(currentCellValue == thisScore):
                    if(closestScoreIndexStartRange == -1):
                        closestScoreIndexStartRange = cellIndex
                    closestScoreIndexEndRange = cellIndex
            if(cellIndex == closestScoreIndexStartRange):
                value = float(sheet.cell(percentileRow, closestScoreIndexStartRange+percentileStartCol).value)
                percentileOfThisTime = PercentileValue(startRange=value)
            elif(closestScoreIndexStartRange < 0):
                value = float(sheet.cell(percentileRow, percentileStartCol).value)
                percentileOfThisTime = PercentileValue(endRange=value)
            elif(closestScoreIndexStartRange == closestScoreIndexEndRange):
                value = float(sheet.cell(percentileRow, closestScoreIndexStartRange+percentileStartCol).value)
                percentileOfThisTime = PercentileValue(value=value)
            else:
                value1 = float(sheet.cell(percentileRow, closestScoreIndexStartRange+percentileStartCol).value)
                value2 = float(sheet.cell(percentileRow, closestScoreIndexStartRange+percentileStartCol).value)
                percentileOfThisTime = PercentileValue(startRange=value1, endRange=value2)
            percentileOfThisTest.append(percentileOfThisTime)
            
        percentiles.append(percentileOfThisTest)
    return percentiles

# Return 2D array, first dimension corresponds to tests and second contains potential range of "less, as, or greater"
# Array is ordered the same as the testNamesForSheets
def getProgress(GMFCSLevel, percentiles):
    progress = []

    for testIndex in range(numTests):

        # Get potential range of difference
        pastPercentile = percentiles[testIndex][0]
        currentPercentile = percentiles[testIndex][1]
        maxDifference = currentPercentile.endRange - pastPercentile.startRange
        minDifference = currentPercentile.startRange - pastPercentile.endRange
        difference = [minDifference, maxDifference]

        centileChangeRow = mapForDifferenceSheets.get(testNamesForSheets[testIndex])

        thisProgress = []
        # First check if change is under lower bound, then in between bounds, then above upper bound
        if(difference[0] < centileChange[0][centileChangeRow].value):
            thisProgress.append('l')
        if(difference[1] > centileChange[0][centileChangeRow].value and difference[0] < centileChange[1][centileChangeRow].value):
            thisProgress.append('a')
        if(difference[1] > centileChange[1][centileChangeRow].value):
            thisProgress.append('m')
        progress.append(thisProgress)
    
    return progress

percentiles = getPerentiles(GMFCSLevel, age, scores) 
progress = getProgress(GMFCSLevel, percentiles) 
   
print(progress)