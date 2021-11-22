import csv
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *
from numpy import *
import sys

"""    
Steps acomplised in this file
A. Read file into memoy, remove first line
B. 
"""
print("\n\n\nReading file into memory")
with open('COVIDDeathData_CountyOfResidence 2021_11_15.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
print("Finished reading file: " + str(len(data)))
del data[0]
"""
0 County
1 Sex
2 Age Range, '0-19','20-29','30-39','40-49','50-59','60-69','70-79','80+'
3 Onset Date  (m/d/y)
4 Admission Date
5 Date Of Death 
6 Case Count
7 Hospitalized Count
8 Death Due To Illness Count - County Of Death
9 State of Death
10 State of Residence
11 Onset Date (added)
"""

"""
0 Onset Year-month
1 Age, 10,20,30,40,50,60,70,80
"""
#print (str(data[0]))
#sys.exit()


print("Loading arrays..")
UniqueAge = [10,20,30,40,50,60,70,80]
UniqueAgeStr = ['0-19','20-29', '30-39','40-49','50-59','60-69','70-79','80+'] 
AgeConvert = {'0-19':10,'20-29':20, '30-39':30,'40-49':40,'50-59':50,'60-69':60,'70-79':70,'80+':80 }
DeathData=[]
HospitalData=[]
InfectionData=[]
tmpDate=[]
temp=[]
for phrase in data:
    try:
        if int(phrase[8]) > 0:
            tmpDate=phrase[5].split("-")
            temp = phrase + [str(tmpDate[0])+ "-" + str(tmpDate[1])]
            for x in range(int(temp[8])):
                DeathData.append([temp[9], AgeConvert[temp[2]]])
                if temp[2]=='0-19':
                    print (str(phrase))
        elif int(phrase[7]) > 0:
            tmpDate=phrase[3].split("-")
            temp = phrase + [str(tmpDate[0])+ "-" + str(tmpDate[1])]
            for x in range(int(phrase[7])):
                HospitalData.append([temp[9], AgeConvert[temp[2]]])
        else:  
            tmpDate=phrase[3].split("-")
            temp = phrase + [str(tmpDate[0])+ "-" + str(tmpDate[1])]
            for x in range(int(phrase[6])):
                InfectionData.append([temp[9], AgeConvert[temp[2]]])
    except:
        print("Error found")
        print(str(phrase)+"\n")
        sys.exit()

del tmpDate, temp
print("Loading complete\n")

print("Death data line 0 = " + str(DeathData[0]))
for tmp in DeathData:
    if tmp[0] == 10:
        print(str(tmp))
#sys.exit()






#
# Lets get the unique months covered in the data
#
UniqueMonths = [row[0] for row in InfectionData]
UniqueMonths = set(UniqueMonths)
UniqueMonths = (list(UniqueMonths))
UniqueMonths.sort()
print("Unique Months: " + str(UniqueMonths))
#print("Unique months: " + str(UniqueMonths))
#print("Length: " + str(len(UniqueMonths)))

print(str(UniqueAge))
# lets build a table for number of people death
print("Building death data")
MonthlyDeathData = [[""] + UniqueMonths]
CurrentAgeData=[]
PatientCount=0
LineCount = 0
for age in UniqueAge:
    CurrentAgeData = [age]
    for month in UniqueMonths:
        PatientCount = 0
        for PatientRecord in DeathData:
            if (PatientRecord[0] == month):
                if (PatientRecord[1] == age and PatientRecord[1] == age):
                    PatientCount = PatientCount + 1
        CurrentAgeData.append(PatientCount)
    MonthlyDeathData.append(CurrentAgeData)
print("Finished")

with open("new_file_DeathDataRaw.csv","w+") as my_csv:
  csvWriter = csv.writer(my_csv,delimiter=',')
  csvWriter.writerows(MonthlyDeathData)


# lets build a table for number of people hospitalized
print("Building Hospital data")
MonthlyHospitalData = [[""] + UniqueMonths]
CurrentAgeData=[]
PatientCount=0
LineCount = 0
for age in UniqueAge:
    CurrentAgeData = [age]
    for month in UniqueMonths:
        PatientCount = 0
        for PatientRecord in HospitalData:
            if (PatientRecord[0] == month):
                if (PatientRecord[1] == age and PatientRecord[1] == age):
                    PatientCount = PatientCount + 1
        CurrentAgeData.append(PatientCount)
    MonthlyHospitalData.append(CurrentAgeData)
print("Finished")

with open("new_file_HospitalDataRaw.csv","w+") as my_csv:
  csvWriter = csv.writer(my_csv,delimiter=',')
  csvWriter.writerows(MonthlyHospitalData)

# lets build a table for number of people infected
print("Building Infected data")

MonthlyInfectedData = [[""] + UniqueMonths]
CurrentAgeData=[]
PatientCount=0
LineCount = 0
for age in UniqueAge:
    CurrentAgeData = [age]
    for month in UniqueMonths:
        PatientCount = 0
        for PatientRecord in InfectionData:
            if (PatientRecord[0] == month):
                if (PatientRecord[1] == age and PatientRecord[1] == age):
                    PatientCount = PatientCount + 1
        CurrentAgeData.append(PatientCount)
    MonthlyInfectedData.append(CurrentAgeData)
print("Finished")

with open("new_file_InfectedDataRaw.csv","w+") as my_csv:
  csvWriter = csv.writer(my_csv,delimiter=',')
  csvWriter.writerows(MonthlyInfectedData)


'''x=numpy.array (list)
numpy.unique (x) 
'''










'''print("Looking activity by age: ")'''
'''For 50s, cases:217,861    Hospitalization: 12,268    Death: 1,710'''

AgeRange = [10,20,30,40,50,60,70,80]
casecount = 0
Hospitalizationcount = 0
deathcount = 0
for x in range(len(AgeRange)):
    for temp in InfectionData:
        if temp[1] == 50:
            casecount = casecount + 1
    for temp in HospitalData:
        if temp[1] == 50:
            Hospitalizationcount = Hospitalizationcount + 1
    for temp in DeathData:
        if temp[1] == 50:
            deathcount = deathcount + 1





'''Sanity check
1,542,911
79,773
24,527
'''

print("Total deaths: " + str(len(DeathData)) + ", should be 24,527")
print("Hospital total: " + str(len(HospitalData)), ", should be 79,773")
print("Infected total: " + str(len(InfectionData)+len(HospitalData)), ", should be 1,542,911")
print ("Hello World")

