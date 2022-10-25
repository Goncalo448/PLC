import re
import math

#(a) frequência de processos por ano

#r'([A-Z][a-z]+| )+'
#filtro que dá sempre a última palavra de uma seq de palavras

def freq_by_years(file):
    dic_by_years = {}

    for line in file:
        slices = re.split(r'[::-]', line)
        if len(slices) > 1:
            if slices[2] not in dic_by_years.keys():
                dic_by_years[slices[2]] = []

            dic_by_years[slices[2]].append(line)

    return dic_by_years


def getFirstName(person, dic, year):
    firstName = re.split(r'\s+', person)
    if re.fullmatch(r'[A-Z][a-z]+', firstName[-1]):
        if firstName[-1] not in dic[year].keys():
            dic[year][firstName[-1]] = 0
        dic[year][firstName[-1]] += 1

    return 0


def getLastName(person, dic, year):
    lastName = re.split(r'\s+\n+', person)
    if re.fullmatch(r'[A-Z][a-z]+', lastName[-1]):
        if lastName[-1] not in dic[year].keys():
            dic[year][lastName[-1]] = 0
        dic[year][lastName[-1]] += 1

    return 0


#EXISTEM CASOS A SER IGNORADOS
def freq_by_centuries(file):

    dic_by_centuries = {}
    for line in file:
        slices = re.split(r'::|,|\.', line)
        print(slices)
        if len(slices) >= 2:
            date = re.split(r'-', slices[1])
            
            if date[0] not in dic_by_centuries.keys():
                dic_by_centuries[date[0]] = {}
            
            dad = slices[3]
            mom = slices[4]
            getFirstName(dad, dic_by_centuries, date[0])
            getLastName(dad, dic_by_centuries, date[0])
            getFirstName(mom, dic_by_centuries, date[0])
            getLastName(mom, dic_by_centuries, date[0])

    print(dic_by_centuries)

    return


'''def freq_by_relationship(file):

    dic_by_centuries = {}
    for line in file:
        slices = re.split(r'::', line)
        if slices[1] not in dic_by_centuries.keys():
            dic_by_centuries[slices[1]] = {}
        
        dad = slices[3]
        mom = slices[4]
        


    return'''


file = open("processos.txt", "r")
freq_by_centuries(file)
#dic = freq_by_years(file)

#for key in sorted(dic.keys()):
 #   print(str(key) + ": " + str(len(dic[key])))




