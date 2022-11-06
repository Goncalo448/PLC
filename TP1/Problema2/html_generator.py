import a
import b
import c
import d
import e
import json
import re


def generate_pagina_indicador(char):
	with open("pagina_indicador_"+char+".html", "w") as file:
		content ="""<!DOCTYPE html>
					<html>
					<h1>Página do indicador</h1>
					<body>
					<li><a href="index.html">Página principal</a></li>
					</body>
					</html>"""

		file.write(content)


def html_a():
	generate_pagina_indicador("a")

	content = """<h3>A - Datas extremas:</h3>
				<li><a href="pagina_indicador_a.html">Página do Indicador</a></li>
				<p>datas</p>
				<br></br>"""
	dic = a.datas_extremas()
	dic_in_json = json.dumps(dic)

	content = re.sub(r'datas', dic_in_json, content)

	return content


def html_b():
	generate_pagina_indicador("b")

	content = """<h3>Distribuição por modalidade em cada ano e no total:</h3>
				<li><a href="pagina_indicador_b.html">Página do Indicador</a></li>
				<p>-ano-</p>
				<p>-total-</p>
				<br></br>"""

	dic_por_ano = b.distribuicao_modalidade_ano()
	dic_total = b.distribuicao_modalidade_total()

	#dic_por_ano_json = json.dumps(dic_por_ano)
	#dic_total_json = json.dumps(dic_total)

	dic_por_ano_str = ""
	for ano in dic_por_ano.keys():
		dic_por_ano_str += str(ano) + ":<br>"
		for modalidade in dic_por_ano[ano].keys():
			dic_por_ano_str += modalidade + ": " + str(dic_por_ano[ano][modalidade]) + "; "
		dic_por_ano_str += "<br></br>"

	dic_total_str = "Total:<br>"
	for modalidade in dic_total.keys():
		dic_total_str += modalidade + ": " + str(dic_total[modalidade]) + "; "

	content = re.sub(r'-ano-', dic_por_ano_str, content)
	content = re.sub(r'-total-', dic_total_str, content)

	return content


def html_c():
	generate_pagina_indicador("c")

	content = """<h3>Distribuição por idade e género (para a idade, considera apenas 2 escalões: < 35 anos e >= 35):</h3>
				<li><a href="pagina_indicador_c.html">Página do Indicador</a></li>
				<p>-genero-</p>
				<p>-idade-</p>
				<br></br>"""

	dic_genero = c.distribuicao_genero()
	dic_idade = c.distribuicao_idade()

	dic_genero_json = json.dumps(dic_genero)
	dic_idade_json = json.dumps(dic_idade)

	content = re.sub(r'-genero-', dic_genero_json, content)
	content = re.sub(r'-idade-', dic_idade_json, content)

	return content


def html_d():
	generate_pagina_indicador("d")

	content = """<h3>Distribuição por morada:</h3>
				<li><a href="pagina_indicador_d.html">Página do Indicador</a></li>
				<p>-morada-</p>
				<br></br>"""

	dic_morada = d.distribuicao_morada()
	dic_morada_json = json.dumps(dic_morada)

	content = re.sub(r'-morada-', dic_morada_json, content)

	return content


def html_e():
	generate_pagina_indicador("e")

	content = """<h3>Percentagem de aptos e não aptos por ano:</h3>
				<li><a href="pagina_indicador_e.html">Página do Indicador</a></li>
				<p>-aptos-</p>
				<br></br>"""

	dic_aptos_naptos = e.percentagem_aptos_naptos()
	dic_aptos_naptos_json = json.dumps(dic_aptos_naptos)

	content = re.sub(r'-aptos-', dic_aptos_naptos_json, content)

	return content



def generate_html():

	with open("index.html", 'w') as file:
		content = """<!DOCTYPE html>
					<html>
					<h1>Página principal</h1>
					<body>
					-a-
					-b-
					-c-
					-d-
					-e-
					</body>
					</html>"""

		content = re.sub(r'-a-', html_a(), content)
		content = re.sub(r'-b-', html_b(), content)
		content = re.sub(r'-c-', html_c(), content)
		content = re.sub(r'-d-', html_d(), content)
		content = re.sub(r'-e-', html_e(), content)

		file.write(content)


generate_html()