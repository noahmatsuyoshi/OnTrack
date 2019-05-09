import numpy
from fpdf import FPDF
import xlrd

file_name = "data.xlsx"
workbook = xlrd.open_workbook(file_name)



print(xlrd.sheet.Sheet(workbook).__str__)