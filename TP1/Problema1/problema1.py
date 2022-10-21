import re

file = open("processos.txt", "r")

#(a) frequência de processos por ano

filtered_by_proc = []
dic_by_years = {}

for line in file:
    match = re.search(r'(?i:proc).*', line) #já tem todos os processosn(os que existem)

    if match:
        filtered_by_proc.append(line)

for line in filtered_by_proc:
    slices = re.split(r'[::-]', line)
    
    if slices[2] not in dic_by_years.keys():
        dic_by_years[slices[2]] = []

    dic_by_years[slices[2]].append(line)


for key in sorted(dic_by_years.keys()):
    print(str(key) + ": " + str(len(dic_by_years[key])))


