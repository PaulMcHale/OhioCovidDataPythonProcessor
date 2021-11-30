
import sys
import os
import ReadFile


myReadFile = ReadFile.ReadFileUtil("Test")

myReadFile.ParseFileIntoArrays()
myReadFile.GenerateCSVFiles()
myReadFile.PrintStastics()

# myStr = os.getcwd()
# print("Current working directory: " + myStr)



sys.exit()