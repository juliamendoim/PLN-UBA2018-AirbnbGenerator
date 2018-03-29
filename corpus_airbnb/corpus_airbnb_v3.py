#librería de testing y de parseo de htmñ
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import re
import codecs

#Abre chromedriver.exe que necesita Selenium

#Lista todas las url que extrae de cada página que abre para después acceder a esos links 
urls_extraidas = []

#Recorre todas las páginas internas por el range del offset de la página de airbnb. Parsea el html
a = {}
for n in range(0,17):
	a[n] = webdriver.Chrome(executable_path=r'/Users/juliamilanese/Desktop/airbnb/chromedriver')
	a[n].get('https://www.airbnb.com.ar/s/Argentina/homes?refinement_paths%5B%5D=%2Fhomes&place_id=ChIJZ8b99fXKvJURqA_wKpl3Lz0&allow_override%5B%5D=&s_tag=-LFL7cg&section_offset='+str(n)) #/s/san-telmo/homes')
	soup = BeautifulSoup(a[n].page_source, 'html.parser')
	
#Extrae los links de cada aviso, internos a la "home page" solo si contiene el prefijo "rooms"
	for link in soup.findAll('a', href=True):
	    x = link.get('href')
	    if '/rooms' in x:
	    	#print(x)
	    	urls_extraidas.append(x)

#print (urls_extraidas)
#Compila la regex que extrae el número de aviso que va a usar cuando nombre los archivos

regex = re.compile(r'/rooms/(\d+)\?')
browser = webdriver.Chrome(executable_path=r'/Users/juliamilanese/Desktop/airbnb/chromedriver')
#Abre la página de cada aviso interno a la "home page" y lo guardo como html
# for url in urls_extraidas:
# 	chicho = regex.match(url).group(1)
# 	browser.get('https://www.airbnb.com.ar'+str(url))
# 	soup = BeautifulSoup(browser.page_source, 'html.parser')
# 	with open('/Users/juliamilanese/Desktop/corpus_airbnb/html/'+str(chicho)+'.html', 'w') as f:
# 		f.write(browser.page_source)


#Abre el json de los reviews con el key sacado de la url (ver Network) que "muere" después de unas horas. 
#Lo abre una vez, busca el count, y setea el offset de cada review, vuelve a entrar cambiando el offset.
#Lo parsea con la librería json para sacar el reviews count.

for url in urls_extraidas:
	chicho = regex.match(url).group(1)
	offset = 0
	cantidad = 100
	browser.get('https://www.airbnb.com.ar/api/v2/reviews?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=ARS&locale=es-419&listing_id='+chicho+'&role=guest&_format=for_p3&_limit=' + str(cantidad) + '&_offset=' + str(offset) + '&_order=language_country')
	pre = browser.find_element_by_tag_name("pre").text
	data = json.loads(pre)
	count = data['metadata']['reviews_count']
	with codecs.open('/Users/juliamilanese/Desktop/corpus_airbnb/reviews/'+str(chicho)+'.json', 'w','utf-8') as ff:
		ff.write(pre)
	# for n in range(1,int(count/cantidad)+1):
	# 	offset = n*cantidad
	# 	browser.get('https://www.airbnb.com.ar/api/v2/reviews?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=ARS&locale=es-419&listing_id='+chicho+'&role=guest&_format=for_p3&_limit=' + str(cantidad) + '&_offset=' + str(offset) + '&_order=language_country')
	# 	pre = browser.find_element_by_tag_name("pre").text
	# 	data = json.loads(pre)
	# 	count = data['metadata']['reviews_count']
	# 	with codecs.open('/Users/juliamilanese/Desktop/airbnb/'+str(chicho)+'-'+str(offset)+'.json', 'w','utf-8') as ff:
	# 		ff.write(pre)
	
	