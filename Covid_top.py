
import sys
import os
import ReadFile


myReadFile = ReadFile.ReadFileUtil("COVIDDeathData_CountyOfResidence 2021_11_28.csv")

myReadFile.ParseFileIntoArrays()
myReadFile.PrintStastics()
myReadFile.GenerateCSVFiles()
myReadFile.PrintStastics()


sys.exit()