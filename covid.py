import csv
import math
import collections
import re

def covid(file):
    with open(file) as covidtrain:
        with open('covidResult.csv','w') as f:
            reader = csv.reader(covidtrain)
            covidTrainList = list(reader)
            writer = csv.writer(f,delimiter =',')
            latitude = {}
            longitude = {}
            cities = {}
            symptomlist = {}
            provincessymptom = {}
            provincescity = {}
            for i in range(1,len(covidTrainList)):
                #1.1 - Calculating Age Average
                if "-" in covidTrainList[i][1]:
                    first, second = covidTrainList[i][1].split("-")
                    average = round((int(first)+int(second))/2)
                    covidTrainList[i][1] = str(average)
                #1.2 - Changing date format
                d1,m1,y1 = covidTrainList[i][8].split(".")
                covidTrainList[i][8] = m1 + "." + d1 + "." + y1
                d2,m2,y2 = covidTrainList[i][9].split(".")
                covidTrainList[i][9] = m2 + "." + d2 + "." + y2
                d3,m3,y3 = covidTrainList[i][10].split(".")
                covidTrainList[i][10] = m3 + "." + d3 + "." + y3
            for i in range(1,len(covidTrainList)):
                #1.3 - Filling lat/long values
                if covidTrainList[i][6] != 'NaN':
                    if covidTrainList[i][4] in latitude:
                        latitude[covidTrainList[i][4]].append(covidTrainList[i][6])
                    else:
                        latitude[covidTrainList[i][4]] = [covidTrainList[i][6]]
            for i in range(1,len(covidTrainList)):
                if covidTrainList[i][7] != 'NaN':
                    if covidTrainList[i][4] in longitude:
                        longitude[covidTrainList[i][4]].append(covidTrainList[i][7])
                    else:
                        longitude[covidTrainList[i][4]] = [covidTrainList[i][7]]
            for i in range(1,len(covidTrainList)):
                if covidTrainList[i][6] == 'NaN':
                    latsum = 0
                    for elem in latitude[covidTrainList[i][4]]:
                        latsum += float(elem)
                    averageLat = latsum/len(latitude[covidTrainList[i][4]])
                    averageLat = round(averageLat,2)
                    covidTrainList[i][6] = str(averageLat)
                if covidTrainList[i][7] == 'NaN':
                    longsum = 0
                    for elem in longitude[covidTrainList[i][4]]:
                        longsum += float(elem)
                    averageLong = longsum/len(latitude[covidTrainList[i][4]])
                    averageLong = round(averageLong,2)
                    covidTrainList[i][7] = str(averageLong)
            for i in range(1,len(covidTrainList)):
                if covidTrainList[i][4] in cities and covidTrainList[i][3] != 'NaN':
                    cities[covidTrainList[i][4]].append(covidTrainList[i][3])
                elif covidTrainList[i][3] != 'NaN':
                    cities[covidTrainList[i][4]] = [covidTrainList[i][3]]
            for keys in cities:
                #1.4 - Filling province/city value
                provincescity[keys] = {}
            for keys in cities:
                for x in cities[keys]:
                    if x.strip() in provincescity[keys]:
                        provincescity[keys][x.strip()] += 1
                    else:
                        provincescity[keys][x.strip()] = 1
            for keys in provincescity:
                temp1 = provincescity[keys]
                sorted_temp1 = sorted(temp1.items(),key = lambda x:x[1],reverse = True)
                provincescity[keys] = sorted_temp1
            for keys in provincescity:
                for i in range(0, len(provincescity[keys])):
                    for j in range(i+1,len(provincescity[keys])):
                        temp2 = ''
                        if provincescity[keys][i][1] == provincescity[keys][j][1] and provincescity[keys][i][0] > provincescity[keys][j][0]:
                            temp2 = provincescity[keys][i]
                            provincescity[keys][i] = provincescity[keys][j]
                            provincescity[keys][j] = temp2
            for i in range(1,len(covidTrainList)):
                if covidTrainList[i][3] == 'NaN':
                    popularcity = provincescity[covidTrainList[i][4]][0][0]
                    covidTrainList[i][3] = str(popularcity)
            for i in range(1,len(covidTrainList)):
                if covidTrainList[i][4] in symptomlist:
                    x = covidTrainList[i][11].split(";")
                    for elem in x:
                        elem = elem.strip()
                        if elem != 'NaN':
                            symptomlist[covidTrainList[i][4]].append(elem)
                else:
                    x = covidTrainList[i][11].split(";")
                    for elem in x:
                        elem = elem.strip()
                    symptomlist[covidTrainList[i][4]] = [x[0]]
                    for i in range(1,len(x)):
                        if x[i] != 'NaN':
                            symptomlist[covidTrainList[i][4]].append(x[i])
            for keys in symptomlist:
                provincessymptom[keys] = {}
            for keys in symptomlist:
                for x in symptomlist[keys]:
                    if x.strip() in provincessymptom[keys]:
                        provincessymptom[keys][x.strip()] += 1
                    else:
                        provincessymptom[keys][x.strip()] = 1
            for keys in provincessymptom:
                temp = provincessymptom[keys]
                sorted_temp = (sorted(temp.items(),key = lambda x: x[1], reverse = True))
                provincessymptom[keys] = sorted_temp
            for keys in provincessymptom:
                for i in range(0, len(provincessymptom[keys])):
                    for j in range(i+1,len(provincessymptom[keys])):
                        temp = ''
                        if provincessymptom[keys][i][1] == provincessymptom[keys][j][1] and provincessymptom[keys][i][0] > provincessymptom[keys][j][0]:
                            temp = provincessymptom[keys][i]
                            provincessymptom[keys][i] = provincessymptom[keys][j]
                            provincessymptom[keys][j] = temp
            for i in range(1,len(covidTrainList)):
                if covidTrainList[i][11] == 'NaN':
                    popularsymptom = provincessymptom[covidTrainList[i][4]][0][0]
                    covidTrainList[i][11] = popularsymptom
            writer.writerows(covidTrainList)
    covidtrain.close()
    f.close()


covid('covidTrain.csv') 
