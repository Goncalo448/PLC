import re
import json
import os


path = os.getcwd()

def first_20_lines(file):
	dic = {}

	with file as myfile:
		for x in range(20):
			if x not in dic.keys():
				dic[x] = None
			dic[x] = next(myfile)

	return dic


def write_into_json_file(dic):
	json_string = json.dumps(dic)

	if os.path.isfile(path + "/output.json"):
		with open("output.json", 'w') as outfile:
			json.dump(json_string, outfile)
	else:
		json_file = open("output.json", 'x')
		json.dump(json_string, json_file)


file = open("processos.txt", "r")
dic = first_20_lines(file)
write_into_json_file(dic)

