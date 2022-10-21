import re

f = open("processos.txt", "r")

#(a) frequência de processos por ano

for linha in f:
    filter_by_proc = re.search(r'(?i:proc).*', linha) #já tem todos os processosn(os que existem)
    if filter_by_proc:
        




