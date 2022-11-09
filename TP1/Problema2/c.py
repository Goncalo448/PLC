import re


def distribuicao_genero():
    dic = {}

    with open("emd.csv", 'r') as myfile:
    	next(myfile)
    	for line in myfile:
	        slices = re.split(r',',line)
	        
	        for slice in slices:
	        	if re.fullmatch(r'[A-Z]', slice):
	        		genero = slice
	        		break

	        if genero not in dic.keys():
	            dic[genero] = 0
	        dic[genero] += 1

    return dic


def distribuicao_idade():
	dic = {}
	dic["<35"] = 0
	dic[">35"] = 0
	with open("emd.csv", 'r') as myfile:
		next(myfile)
		for line in myfile:
			slices = re.split(r',', line)
			idade = slices[5]

			if int(idade) < 35:
				dic["<35"] += 1
			else:
				dic[">35"] += 1

	return dic


#dic_genero = distribuicao_genero()
#dic_idade = distribuicao_idade()
#print(dic_idade)