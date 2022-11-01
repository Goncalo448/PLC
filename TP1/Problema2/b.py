import re

#Distribuição por modalidade em cada ano e no total;

def distribuicao_modalidade_total():
	dic = {}
	with open("emd.csv", 'r') as myfile:
		next(myfile)
		for line in myfile:
			slices = re.split(r',', line)
			modalidade = slices[8]
			
			if modalidade not in dic.keys():
				dic[modalidade] = 0

			dic[modalidade] += 1

	return dic


def distribuicao_modalidade_ano():
	dic = {}
	with open("emd.csv", 'r') as myfile:
		next(myfile)
		for line in myfile:
			slices = re.split(r',', line)
			modalidade = slices[8]

			match = re.match(r'[0-9]{4}', slices[2])
			if match:
				ano = int(match.group())

			if ano not in dic.keys():
				dic[ano] = {}

			if modalidade not in dic[ano].keys():
				dic[ano][modalidade] = 0

			dic[ano][modalidade] += 1

	return dic


dic_total = distribuicao_modalidade_total()
dic_ano = distribuicao_modalidade_ano()