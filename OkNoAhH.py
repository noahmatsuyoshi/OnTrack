import csv
import statistics
import numpy
from fpdf import FPDF
import os

filePath = "test1.pdf"

if(os.path.isfile(filePath)):
    os.remove(filePath)
pdf = FPDF()
pdf.add_page()
pdf.set_xy(10, 10)
with open('ECAB_Level_3.csv') as csv_file:
    csv.reader=csv.reader(csv_file,delimiter=',')
    next(csv.reader)
    row_num=0
    for row in csv.reader:
        max = float(row[0])
        row_num +=1
        sum = 0
        for i in range(len(row)):
            sum += float(row[i])
            if float(row[i])>max:
                max=float(row[i])
        average = sum/len(row)
        pdf.set_font('Times', 'B', 13.0)
        pdf.cell(ln=2, h=7.0, align='L', w=18, txt="Row "+ str(row_num), border=1)
        pdf.set_font('Times', 'B', 10.0)
        pdf.cell(ln=2, h=5.0, align='L', w=0, txt="std deviation is % s " % (round(statistics.stdev(numpy.float_(row)),3)), border=0)
        pdf.cell(ln=2, h=5.0, align='L', w=0, txt="max is " + str(max), border=0)
        pdf.cell(ln=2, h=5.0, align='L', w=0, txt="average is " + str(round(average,3)), border=0)
pdf.output('test1.pdf', 'F')



