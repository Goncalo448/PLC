import re


def distribuicao_morada(file):
	dic = {}

	with open(file, 'r') as myfile:
		next(myfile)

		for line in myfile:
			slices = re.split(r',', line)
			morada = slices[7]

			if morada not in dic.keys():
				dic[morada] = 0
			dic[morada] += 1

	return dic


file = "emd.csv"
dic_morada = distribuicao_morada(file)
print(dic_morada)