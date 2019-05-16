import numpy
from fpdf import FPDF
import xlrd
import os 

# Inputs (Assume inputs are valid at this point, will handle validation in web form)
GMFCSLevel = "III"
age = [[3, 5], [4, 3]] # [[past year, past month], [current year, current month]]

# Assign scores in this order: "ECAB", "SMWT", "SAROMM", "CEDLpar", "CEDLsc", "EASE", "FSA", "HEALTH", "GMFM"
# With first element being past score and second current
scores = [[25, 30], [25, 30], [25, 30], [25, 30], [25, 30], [25, 30], [25, 30], [25, 30], [25, 30]]

def getRowNumFromAge(age):
    monthRow = round(age[1]/3)
    return age[0]*4+monthRow-6

def findStartAndEndCol(cells):
    startAndEnd = []
    for index in range(len(cells)):
        if(cells[index].ctype == 2 and len(startAndEnd) == 0):
            startAndEnd.append(index)
        elif(cells[index].ctype != 2 and len(startAndEnd) == 1):
            startAndEnd.append(index-1)
            return startAndEnd


file_name = "data.xlsx"
testNames = ["ECAB", "SMWT", "SAROMM", "CEDLpar", "CEDLsc", "EASE", "FSA", "HEALTH", "GMFM"]
#testNames = ["ECAB"] #For testing run only ECAB
percentileRow = 1

numTests = len(testNames)
workbook = xlrd.open_workbook(file_name)
percentiles = numpy.zeros((numTests, 2))

for testIndex in range(numTests):
    sheetName = testNames[testIndex]+"_Level_"+GMFCSLevel
    sheet = workbook.sheet_by_name(sheetName)
    
    for timeIndex in range(2):
        row = getRowNumFromAge(age[timeIndex])
        selectedRow = sheet.row(row)
        
        [percentileStartCol, percentileEndCol] = findStartAndEndCol(selectedRow)
        selectedRow = sheet.row_slice(row, percentileStartCol, percentileEndCol)
        #closestScore = min(selectedRow, key = lambda x:abs(x.value - ECABScore[0]))
        closestScoreIndex = 0
        for cellIndex in range(len(selectedRow)):
            
            if(float(selectedRow[cellIndex].value) <= scores[testIndex][timeIndex]):
                closestScoreIndex = cellIndex
        percentiles[testIndex][timeIndex] = float(sheet.cell(percentileRow, closestScoreIndex+percentileStartCol).value)

print(percentiles)