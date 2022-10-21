import re

file = open("processos.txt", "r")

#(a) frequência de processos por ano

filtered_by_proc = []
for line in file:
    match = re.search(r'(?i:proc).*', line) #já tem todos os processosn(os que existem)

    if match:
        filtered_by_proc.append(line)

for linha in filtered_by_proc:
    match = re.search(r'')


