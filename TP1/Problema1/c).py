import re


def freq_by_relationship(file):
	
	dic_by_relation = {}
	for line in file:
		match = re.search(r'(,)+[A-Z][a-z]+(\s|[A-Z][a-z]+)*\.', line)
		if match:
			relationship = match.group()
			relationship = relationship.lstrip(",")
			relationship = relationship.rstrip(".")
			
			if relationship not in dic_by_relation.keys():
				dic_by_relation[relationship] = 0

			dic_by_relation[relationship] += 1

	return dic_by_relation


file = open("processos.txt", "r")
dic = freq_by_relationship(file)

for relationship in dic.keys():
	print(relationship + ": " + str(dic[relationship]))