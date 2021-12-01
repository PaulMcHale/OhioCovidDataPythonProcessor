import csv
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *
from numpy import *
import sys

class ReadFileUtil:
    def __init__(self, InputFile):
        self.UniqueAge = [10,20,30,40,50,60,70,80]
        self.UniqueAgeStr = ['0-19','20-29', '30-39','40-49','50-59','60-69','70-79','80+'] 
        self.GenerateCSVFiles
        self.AgeConvert = {'0-19':10,'20-29':20, '30-39':30,'40-49':40,'50-59':50,'60-69':60,'70-79':70,'80+':80 }
        self.DeathData=[]
        self.HospitalData=[]
        self.InfectionData=[]
        self.data = []
        """    
        Steps accomplised in this file
        A. Read file into memoy, remove first line
        B. 
        """
        print("\n\n\nReadFileUtil: Reading file into memory")
        with open(InputFile, newline='') as f:
            self.reader = csv.reader(f)
            self.data = list(self.reader)
        print("ReadFileUtil: Finished reading file: " + str(len(self.data)))
        del self.data[0]
        
    def ParseFileIntoArrays(self):
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
        """

        """
        0 Onset Year-month
        1 Age, 10,20,30,40,50,60,70,80
        """
        print("ParseFileIntoArrays: Loading arrays..")
        tmpDate=[]
        temp=[]
        self.DeathData = []
        self.HospitalData = []
        self.InfectionData = []
        for phrase in self.data:
            try:
                if int(phrase[8]) > 0:
                    tmpDate=phrase[5].split("-")
                    temp = phrase + [str(tmpDate[0])+ "-" + str(tmpDate[1])]
                    for x in range(int(temp[8])):
                        self.DeathData.append([temp[9], self.AgeConvert[temp[2]]])
                        # if temp[2]=='0-19':
                        #     print (str(phrase))
                else:
                    if int(phrase[7]) > 0:
                        tmpDate=phrase[3].split("-")
                        temp = phrase + [str(tmpDate[0])+ "-" + str(tmpDate[1])]
                        for x in range(int(phrase[7])):
                            self.HospitalData.append([temp[9], self.AgeConvert[temp[2]]])
                    if int(phrase[6]) > 0:
                        tmpDate=phrase[3].split("-")
                        temp = phrase + [str(tmpDate[0])+ "-" + str(tmpDate[1])]
                        for x in range(int(phrase[6])):
                            self.InfectionData.append([temp[9], self.AgeConvert[temp[2]]])
            except:
                print("ParseFileIntoArrays: Error found")
                print("ParseFileIntoArrays: " + str(phrase)+"\n")
                sys.exit()

        del tmpDate, temp
        print("ParseFileIntoArrays: Loading complete")


        # print("Total deaths: " + str(len(self.DeathData)) + ", should be 26,483")
        # print("Hospital total: " + str(len(self.HospitalData)), ", should be 85,694")
        # print("Infected total: " + str(len(self.InfectionData)), ", should be 1,677,741")



    def GenerateCSVFiles(self):
        #
        # Lets get the unique months covered in the data
        #
        self.UniqueMonths = [row[0] for row in self.InfectionData]
        self.UniqueMonths = set(self.UniqueMonths)
        self.UniqueMonths = (list(self.UniqueMonths))
        self.UniqueMonths.sort()

        # lets build a table for number of people death
        print("GenerateCSVFiles: Building death data")
        self.MonthlyDeathData = [[""] + self.UniqueMonths]
        self.CurrentAgeData=[]
        self.PatientCount=0
        self.LineCount = 0
        for age in self.UniqueAge:
            self.CurrentAgeData = [age]
            for month in self.UniqueMonths:
                self.PatientCount = 0
                for PatientRecord in self.DeathData:
                    if (PatientRecord[0] == month and PatientRecord[1] == age):
                        self.PatientCount = self.PatientCount + 1
                self.CurrentAgeData.append(self.PatientCount)
            self.MonthlyDeathData.append(self.CurrentAgeData)

        with open("new_file_DeathDataRaw.csv","w") as my_csv:
            csvWriter = csv.writer(my_csv,delimiter=',')
            csvWriter.writerows(self.MonthlyDeathData)

        self.myTotal = 0
        for m in self.MonthlyDeathData[1:]:
            self.myTotal = self.myTotal + sum(m[1:])
        print ("GenerateCSVFiles: Doublecheck: " + str(self.myTotal))
        print("GenerateCSVFiles: Finished")


        # lets build a table for number of people hospitalized
        print("GenerateCSVFiles: Building Hospital data")
        self.MonthlyHospitalData = [[""] + self.UniqueMonths]
        self.CurrentAgeData=[]
        self.PatientCount=0
        LineCount = 0
        for age in self.UniqueAge:
            self.CurrentAgeData = [age]
            for month in self.UniqueMonths:
                self.PatientCount = 0
                for PatientRecord in self.HospitalData:
                    if (PatientRecord[0] == month):
                        if (PatientRecord[1] == age and PatientRecord[1] == age):
                            self.PatientCount = self.PatientCount + 1
                self.CurrentAgeData.append(self.PatientCount)
            self.MonthlyHospitalData.append(self.CurrentAgeData)

        with open("new_file_HospitalDataRaw.csv","w") as my_csv:
            csvWriter = csv.writer(my_csv,delimiter=',')
            csvWriter.writerows(self.MonthlyHospitalData)

        self.myTotal = 0
        for m in self.MonthlyHospitalData[1:]:
            self.myTotal = self.myTotal + sum(m[1:])
        print ("GenerateCSVFiles: Doublecheck: " + str(self.myTotal))
        print("GenerateCSVFiles: Finished")


        # # lets build a table for number of people hospitalized
        # print("Building Hospital data")
        # self.TempData = self.HospitalData # Update
        # self.MonthlyInfectedData = [[""] + self.UniqueMonths]
        # self.CurrentAgeData=[]
        # self.PatientCount=0
        # self.LineCount = 0
        # for age in self.UniqueAge:
        #     self.CurrentAgeData = [age]
        #     for month in self.UniqueMonths:
        #         self.PatientCount = 0
        #         for PatientRecord in self.TempData:
        #             if (PatientRecord[0] == month and PatientRecord[1] == age):
        #                 self.PatientCount = self.PatientCount + 1
        #         self.CurrentAgeData.append(self.PatientCount)
        #     self.MonthlyInfectedData.append(self.CurrentAgeData)
        # self.MonthlyHospitalData = self.TempData   # Update 
        # self.TempData = []
        # with open("new_file_HospitalDataRaw.csv","w") as my_csv:
        #     csvWriter = csv.writer(my_csv,delimiter=',')
        #     csvWriter.writerows(self.MonthlyHospitalData)
        # print("Finished")











        # lets build a table for number of people infected
        print("GenerateCSVFiles: Building Infected data")
        self.TempData = self.InfectionData
        self.MonthlyInfectedData = [[""] + self.UniqueMonths]
        self.CurrentAgeData=[]
        self.PatientCount=0
        self.LineCount = 0
        for age in self.UniqueAge:
            self.CurrentAgeData = [age]
            for month in self.UniqueMonths:
                self.PatientCount = 0
                for PatientRecord in self.TempData:
                    if (PatientRecord[0] == month and PatientRecord[1] == age):
                        self.PatientCount = self.PatientCount + 1
                self.CurrentAgeData.append(self.PatientCount)
            self.MonthlyInfectedData.append(self.CurrentAgeData)
        with open("new_file_InfectedDataRaw.csv","w") as my_csv:
            csvWriter = csv.writer(my_csv,delimiter=',')
            csvWriter.writerows(self.MonthlyInfectedData)

        self.myTotal = 0
        for m in self.MonthlyInfectedData[1:]:
            self.myTotal = self.myTotal + sum(m[1:])
        print ("GenerateCSVFiles: Doublecheck: " + str(self.myTotal))
            
    
        print("GenerateCSVFiles: Finished")


    '''x=numpy.array (list)
    numpy.unique (x) 
    '''
    def PrintStastics(self):
        '''print("Looking activity by age: ")'''
        '''For 50s, cases:217,861    Hospitalization: 12,268    Death: 1,710'''

        # AgeRange = [10,20,30,40,50,60,70,80]
        # self.casecount = 0
        # self.Hospitalizationcount = 0
        # self.deathcount = 0
        # for x in range(len(AgeRange)):
        #     for temp in self.InfectionData:
        #         if temp[1] == 50:
        #             self.casecount = self.casecount + 1
        #     for temp in self.HospitalData:
        #         if temp[1] == 50:
        #             self.Hospitalizationcount = self.Hospitalizationcount + 1
        #     for temp in self.DeathData:
        #         if temp[1] == 50:
        #             self.deathcount = self.deathcount + 1





        '''Sanity check
        1,542,911
        79,773
        24,527
        '''

        print("PrintStastics: Death total: " + str(len(self.DeathData)) + ", should be 26,483")
        print("PrintStastics: Hospital total: " + str(len(self.HospitalData)), ", should be 85,694")
        print("PrintStastics: Infected total: " + str(len(self.InfectionData)), ", should be 1,677,741\n")

