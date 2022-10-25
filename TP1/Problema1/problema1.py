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


def getFirstName(person):
    firstName = re.split(r'\s+', person)
    return firstName[0]


def getLastName(person):
    lastName = re.split(r'\s+', person)
    print(lastName)
    return lastName[-1]


def freq_by_centuries(file):

    dic_by_centuries = {}
    for line in file:
        slices = re.split(r'::', line)
        if slices[1] not in dic_by_centuries.keys():
            dic_by_centuries[slices[1]] = {}
        dad = slices[3]
        mom = slices[4]
        dad_first_name = getFirstName(dad)
        dad_last_name = getLastName(dad)

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




