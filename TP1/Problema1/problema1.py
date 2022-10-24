import re
import math

#(a) frequência de processos por ano

def freq_by_years(file):
    dic_by_years = {}

    for line in file:
        slices = re.split(r'[::-]', line)
        if len(slices) > 1:
            if slices[2] not in dic_by_years.keys():
                dic_by_years[slices[2]] = []

            dic_by_years[slices[2]].append(line)

    return dic_by_years


def freq_by_centuries(file):
    return


def freq_by_relationship(file):

    for line in file:
        slices = re.split(r'[:{2,4}\-{1}.{1}]', line)
        print(slices)
        #for s in slices:
         #   match = re.fullmatch(r'(\w+| )', s)

    return


file = open("processos.txt", "r")
freq_by_relationship(file)
#dic = freq_by_years(file)

#for key in sorted(dic.keys()):
 #   print(str(key) + ": " + str(len(dic[key])))




