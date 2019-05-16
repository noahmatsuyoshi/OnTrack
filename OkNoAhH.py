import numpy
from fpdf import FPDF
import xlrd
import os 

# Inputs (Assume inputs are valid at this point, will handle validation in web form)
GMFCSLevel = "III"
age = [3, 5]

def getRowNumFromAge(age):
    monthRow = round(age[1]/3)
    return age[0]*4+monthRow-6


file_name = "data.xlsx"
#testNames = ["ECAB", "SMWT", "SAROMM", "CEDLpar", "CEDLsc", "EASE", "FSA", "HEALTH", "GMFM"]
testNames = ["ECAB"] #For testing run only ECAB
percentileStartCol = 2
percentileEndColMax = 22 #For longest row

workbook = xlrd.open_workbook(file_name)
row = getRowNumFromAge(age)
for name in testNames:
    sheetName = name+"_Level_"+GMFCSLevel
    sheet = workbook.sheet_by_name(sheetName)
    percentileEndCol = percentileEndColMax
    if(sheetName=="ECAB_Level_I"):
        percentileEndCol = 13
    elif(sheetName=="ECAB_Level_II"):
        percentileEndCol = 18
    selectedRow = sheet.row_slice(row, percentileStartCol, percentileEndCol)
    print(selectedRow[0].value)


