# tecnojob
Buscador de ofertas de empleo - proyecto final

# **CONSTRUIR BASE DE DATOS CON API DE BUSQUEDA DE TRABAJO**

Vamos a recoger ofertas de trabajo desde una API de búsqueda de trabajos.

*   Parte 1: Creación de una base de datos de trabajos con una API.
*   Parte 2: Hacer web scraping para afinar la info que va a la BBDD.
*   Parte 3: Encapsular todo el código en Django.
*   Parte 4: Crear la app de generar CV con los datos de usuario.

## **EMPEZANDO**

En la primera parte del proyecto utilizaremos las siguientes herramientas:

 - [Python](https://www.python.org/)
 - Libreria de analisis de datos [Pandas](https://pandas.pydata.org/)
 - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
 - Libreria de[ peticiones](https://requests.readthedocs.io/en/master/)
 - [PyMySQL](https://pymysql.readthedocs.io/en/latest/)<span
   style="text-decoration:underline;"> </span>Lib

Antes de empezar a programar la app debemos instalar Python y las demás librerias anteriormente mencionadas. Usaremos en concreto Python 3. Tenemos que tener xampp o mysql funcionando en nuestro ordenador. Si no habrá que seguir estas[ pautas de instalación](https://dev.mysql.com/doc/mysql-getting-started/en/).

## Instalando Python:

Instalación a través del[ sitio web oficial](https://www.python.org/downloads/).

## Instalando BeautifulSoup:

Para instalar BeautifulSoup es necesario tener instalado PIP de Python3. Si no está instalado, por favor, seguid esta [guía oficial de instalación](https://pip.pypa.io/en/stable/installing/). Seguidamente escribir:

```
$ pip install beautifulsoup4
```

## Instalando las librerias Request y PyMySQL:

```
$ pip install request
$ pip install PyMySQL
```

## **USANDO LA API**

Existen diferentes APIs de busqueda de trabajo, entre ellas Indeed, Monster, OpcionEmpleo entre otras. Nosotros usaremos la de[ OpcionEmpleo](https://www.careerjet.com/partners/api/).

Existen ventajas y desventajas de utilizar una API para capturar datos. Por ejemplo, proporcionan un proceso mucho más estable para recuperar información que la técnica del web scrapping. Aunque con esta última técnica además se pueden utilizar las etiquetas HTML/CSS para capturar otros datos de interés, y por lo tanto, puede denegarse su acceso cada vez que se cambien estas etiquetas en el frontend. Además, las API normalmente proporcionarán información a través de una sintaxis normalizada (ya sea JSON o XML, en vez de HTML). Las deventajas son las limitaciones de consulta impuestas y el hecho de que podrían desaparecer repentinamente por decisión de su propietario.

Existe una[ librería de Python](https://pypi.org/project/careerjet-api/) disponible para esta API:

## **Instalación de la API**

```
    $ pip install careerjet_api
```

## **Documentación:**

```
    pydoc careerjet_api
```

## **Uso:**

```
from careerjet_api import CareerjetAPIClient
cj  =  CareerjetAPIClient("en_GB")
result_json = cj.search({
	'location': 'london',
    'keywords': 'python',
    'affid': '213e213hd12344552',
    'user_ip': '11.22.33.44',
    'url': 'http://www.example.com/jobsearch?q=python&l=london',
    'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'
})
```

## **Parámetros de búsqueda obligatorios**

*   `affid` :  ID de afiliado proporcionado por CareerJet, en este caso sirve el siguiente token: ‘213e213hd12344552’ .
*   `user_ip` :  dirección IP del usuario final al que se mostrarán los resultados de la búsqueda.
*   `user_agent` :  Agente de usuario del navegador del usuario final.
*   `url` :  URL de la página que mostrará los resultados de la búsqueda.

## **Parámetros de búsqueda opcionales**

*   `keywords`: Palabras clave para que coincidan con el título, el contenido o el nombre de la empresa de una oferta de trabajo.
*   `location`: Ubicación de los trabajos solicitados.
*   `sort`: Tipo de ordenación. Esto puede ser: ‘relevance’(predeterminado) -ordenado por relevancia creciente,- ‘fecha’ -ordenado por fecha decreciente y- ‘salary’ -ordenado por salario decreciente.
*   `start_num`: Posición de las contabilizaciones de trabajo devueltas dentro de todo el espacio de resultados. Deber ser > 1 y &lt; Número de aciertos.
*   `pagesize`: Número de trabajos devueltos en una única llamada.
*   `page`: Número de páginas de los trabajos devueltos dentro de todo el espacio de resultados. Debe ser > 1. Si este valor se configura, se sobrescribe `start_num`.
*   `contracttype`: Tipo de contrato seleccionado.`p` — trabajo permanente, `c` — contrato, `t` — temporal, `i` — formación, `v` — voluntario, ninguno— todos los tipos de contratos.
*   `contractperiod`: Período de contrato seleccionado. `f` — a tiempo completo, `p` — a tiempo parcial, ninguno — todos los períodos de contrato.

## **Código de configuración regional**

El código de configuración regional debe proporcionarse en la construcción del cliente del API. Define la ubicación predeterminada, así como el idioma en el que se devuelven los resultados de la búsqueda. Cada configuración regional corresponde a un sitio de CareerJet.

El valor predeterminado es 'en_GB'.

El código regional a usar es

    :es_ES  => 'http://www.opcionempleo.com'

*   A continuación, utilizaremos la API para recopilar información sobre publicaciones de trabajos basada en las palabras clave y la fecha de búsqueda. 
*   A continuación, rellenaremos una base de datos MySQL con los resultados recuperados.
*   Por último, el proceso principal de web scrapping: obtendremos los datos no proporcionados a través de la API del cliente y los asignaremos a cada publicación de trabajo en nuestra base de datos.

## **IR AL CÓDIGO**

Primero necesitamos crear una secuencia de comandos de Python con las solicitudes de API necesarias. A este archivo lo podemos llamar `careerjet_scraper_api.py`.

```
#importamos el modulo python de la API de Careerjet
from careerjet_api import CareerjetAPIClient
```

Aquí es necesario leer la documentación anterior sobre la API para comprender el código que vamos a crear.

Creamos una variable que contiene la función principal con la localización de procedencia de los trabajos:

```
cj  =  CareerjetAPIClient("en_GB")
```

Ahora necesitamos definir los parámetros de búsqueda que vamos a utilizar. Digamos que estamos buscando un trabajo de desarrollo de Python en Barcelona:

```
result_json = cj.search({
	'location': 'barcelona',
    'keywords': 'python',
    'pagesize': '100',
    'affid': '****************',
    'user_ip': '11.22.33.44',
    'url': 'http://www.example.com/jobsearch?q=python&l=barcelona',
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69'
})
```

Lo que ocurre aquí es lo siguiente. Solamente voy a describir algunos de los valores importantes:

*   `location`: Ubicación. Esto será importante, más adelante.
*   `pagesize`: Máximo de resultados devueltos por consulta.
*   `keywords`: Palabras clave para que coincidan con el título, el contenido o el nombre de la empresa de una oferta de trabajo.
*   `affid` :  ID de afiliado proporcionado por CareerJet, en este caso sirve el siguiente token: ‘213e213hd12344552’ .
*   `user_ip` :  dirección IP del usuario final al que se mostrarán los resultados de la búsqueda.
*   `url` :  URL de la página que mostrará los resultados de la búsqueda.
*   `user_agent` :  El agente de usuario del navegador del usuario final al que se mostrarán los resultados del trabajo. Este campo es obligatorio.

El useragent es la descripción del navegador web. La mayoría de los sitios web lo utilizan para personalizar el contenido dadas las capacidades de un dispositivo en particular y su software. También se utiliza para cuestiones relacionadas con la privacidad.

Ahora vamos a definir nuestra función de búsqueda principal. Llamémoslo `get_offers()`

```
#Nuestra principal función de búsqueda
def get_offers(loc):
	client = CareerjetAPIClient(loc)
	search_results = client.search({})
```

Como parámetros a la función principal le estamos pasando la ubicación geográfica. Por otro lado estamos utilizando el método de búsqueda que devolverá un diccionario de ofertas de trabajo y lo asignará a la variable `search_results`.

Posteriormente nos centraremos en tratar los detalles de cada oferta de trabajo. Necesitamos analizar cada uno de estos elementos para su uso posterior.

```
# recorrer cada elemento de la oferta
for elm in search_results['jobs']:
	offer = (elm['title'],
			 elm['company'],
			 elm['salary'],
			 elm['date'],
			 elm['description'],
			 elm['url'],
			 elm['site'])
```
Cada una de nuestras ofertas será un diccionario de python con la clave principal 'jobs'. Las claves de detalle de la oferta en concreto serán título, compañía, salario, fecha, descripción, url y site.

**Importante**: las ofertas que serán importantes para nosotros serán las que tengan que ver con tecnologías, tic, programación, datos y además como dato adicional que sean en trabajos en remoto.

Todo esto no nos servirá de nada si no podemos almacenar esta información. Luego es el momento de poner en funcionamiento nuestro módulo MySQL y diseñar la base de datos.

## **DISEÑAR LA BASE DE DATOS**

Ahora tenemos que crear un nuevo archivo desde el IDE pycharm y asignarle un nombre, por ejemplo, ``database.py``

```
# usaremos esta función para agregar nuestras ofertas a nuestra base de datos
def addToDatabase(offer):
	# abrir una conexión de base de datos
	db = pymysql.connect (host = "localhost",
						  user = "root",
						  password = '',
						  db = "searchjob",
						  charset = "UTF8"
	)
	# preparar un objeto de cursor usando el método cursor()
	cursor = db.cursor()
```
Comenzamos dando a nuestra función ``addToDatabase`` el argumento ``offer``. Luego el método pymysql.connect se conecta a nuestra base de datos usando los [argumentos requeridos](https://pymysql.readthedocs.io/en/latest/user/examples.html). En realidad charset no es obligatorio, pero se recomienda encarecidamente insertarlo porque la definición del juego de caracteres evitará errores futuros al escribir en la base de datos o mientras se envían datos a la misma.

Ahora agregamos una función para escribir nuestras ofertas en nuestra base de datos:

```
try:
	# Ejecutar procedimiento almacenado SQL
	cursor.execute("CALL sp_insert_data") 
	# Comando SQL insert del Procedimiento Almacenado
	INSERT INTO careerjet (title, company, salary, salary_min, salary_max, date, description, url, site, remote, offer_skills, proposal, proposal_sent) VALUES ('%s', '%s','%s','%s','%s','%s','%s','%s','%s', 'True', 'Undefined', 'None', 'False')
	# Hacer el commit a la base de datos
	db.commit()
except:
	# Revertir en caso de que haya algún error
	db.rollback()
```
Aunque la oferta tenía 9 elementos añadimos 4 nuevas columnas: ``remote``, ``offer_skills``, ``proposal``, ``proposal_sent``.

Y los valores que les pusimos a estas claves respectivamente son: ``True``, ``Undefined``, ``None``, ``False``. Estos campos los necesitaremos más adelante.

Volviendo a nuestro archivo ``careerjet_scraper_api.py`` importamos el módulo ``pymysql`` y la función ``addToDatabase``. Y no olvidemos agregar la llamada a la función.

Nuestro archivo ``careerjet_scraper_api.py`` completo es como sigue:
```
from careerjet_api import CareerjetAPIClient  
  
  
# Desde el archivo database.py importamos la función  
from database import addToDatabase  
  
  
# our main function  
def get_offers(loc):  
  client = CareerjetAPIClient(loc)  
  
  search_results = client.search({  
  'location': 'barcelona',  
        'keywords': 'dba',  
        'sort': 'date',  
        'pagesize': '100',  
        #'page': '5',  
  'affid': '213e213hd12344552',  
        'user_ip': '62.174.168.4',  
        'url': 'http://www.example.com/jobsearch?q=dba&l=barcelona',  
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69'  
  })  
  
  # Devolvemos la lista de resultados  
  offer_list = []  
  
  for elm in search_results['jobs']:  
  offer = (elm.get('title', None),  
                 elm.get('company', None),  
                 elm.get('salary', None),  
                 elm.get('salary_min', None),  
                 elm.get('salary_max', None),  
                 elm.get('date', None),  
                 elm.get('description', None),  
                 elm.get('url', None),  
                 elm.get('site', None))  
  offer_list.append(offer)  
  
  return offer_list  
      # Añadimos la oferta a la Base de Datos (llamando a nuestra función)  
  addToDatabase(offer_list)  
```
Y ahora es el momento de escribir esas ofertas de trabajo en la base de datos llamando a la función principal:
```
if __name__ == '__main__':  
  res = get_offers('es_ES')  
  for offer in res:  
  print(offer)
```
Pero aun no hemos terminado.

## **DANDO UN PASO MÁS**

Abramos una de las páginas de ofertas y veamos si podemos encontrar algunas pistas.

![img_01](https://i.imgur.com/1SsDbwV.png)



Podemos ver una columna de ofertas de trabajo en la derecha y una columna de la izquierda con opciones de búsqueda de trabajo (también conocidos como _parámetros_ ). Además, también hay 2 opciones de búsqueda muy útiles en la parte superior derecha: Titulo del empleo y Ubicación.

También podemos notar que el orden de las ofertas se hace por defecto por _relevancia_. Luego se debería hacer clic en la opción de _fecha_ para obtener la lista de trabajos ordenado por fecha de publicación.

Y como tenemos esta misma opción en nuestra función de parámetros si enviamos una consulta con el parámetro _sort_ configurado para _ordenar por fecha_  `'sort':'date'` , y obtenemos las **las últimas 100 ofertas de trabajo publicadas** en la página de esa ciudad.

**Importante**: Si queremos consultar cada página de la ciudad _n veces_ al día para obtener todas las ofertas publicadas dentro de esas 24 horas debemos automatizar el script para que se ejecute varias veces durante cada día.

Si inspecciona el sitio web de ofertas de cerca encontraremos que existe una [página](https://www.opcionempleo.com/locations/) que enumera todos comunidades autónomas de España.

![img_02](https://i.imgur.com/37Rda3Y.png)


Ahora podemos comenzar a hacer web scraping de esas URL comunitarias primero. Así creamos un archivo Python y lo llamamos `jobapi_get_cities.py`

```
# Importamos nuestros módulos
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Definimos las variables para nuestras fuentes de URL
BASE_URL    = "https://www.opcionempleo.com/" 
regions_URL = "https://www.opcionempleo.com/ofertas-empleo-provincia-de-barcelona-34873.html"

# Las listas que contendrán nuestras comarcas y ciudades
region_URL_list  = []
cities_name_list = []

# Nuestra función para buscar y crear la lista de comarcas
def getRegionLinks(regions_URL):

	# Obtener la fuente de la página de la página URL de comarcas
	html = urlopen(states_URL).read() 
	      
	# Crear el objeto BeautifulSoup   
	soup = BeautifulSoup(html, "lxml")

	# Usamos un método Bs para encontrar la sección de enlaces   
	region_page = soup.find_all(class = "locations")

	# Luego un bucle para obtener los enlaces de todos las comarcas
	# y construimos cada enlace de lsa comarcas usando los relativos   
	for cities in region_page:
		links = cities.findAll('a')
		for a in links:  
			if a.text != '':   
				region_URL_list.append(BASE_URL + a['href'])
				 
	# finalmente devolvemos la lista de URL de los estados   
	return region_URL_list
```
Ahora tenemos una función que devuelve todas las **URL de las páginas de las CCAA** . Y dentro de cada página encontraremos el enlace a cada una de sus ciudades.

Así es como vamos a encontrar cada uno de los **nombres** de las **ciudades** y las  **CCAA** al que pertenecen. Si inspeccionamos el enlace de cada ciudad veremos que el **nombre de** la **ciudad** y **la abreviatura la CCAA** son parte de la cadena URL relativa. Solo necesitamos obtener todas esas cadenas URL y extraer los 2 elementos.

```
# la función para obtener esos nombres de CIUDAD, COMARCA para usar en nuestra API   
def getCityNames ():

	#obtener la lista de URL de estados   
	comarca_URL_list = getStateLinks (states_URL)
	
	# recorrer todas las páginas de estado   
	for page in comarca_URL_list:   
		html = urlopen(página).read()   
		soup = BeautifulSoup(html, "lxml")
		
		#utilice Bs para encontrar los elementos HTML relevantes de las ciudades   
		cities_page = soup.find_all('p', attrs={'class': 'city'})
		
		# recorrer cada elemento para obtener la URL   
		for p in cities_page:   
			links = p.findAll('a')
			 
			# Abrir un archivo txt para almacenar los nombres de las ciudades   
			f = open('cities', 'a', encoding='UTF8') 
			
			# Obtener el enlace de cada ciudad-comarca   
			for a in links:   
				city_region = a['href']
				
				# Parsear los nombres de CIUDAD y COMARCA usando una cadena de URL   
				if city_region[:5] == '/jobs' o '%' in city_state:   
					f.write (a.text + '\n') 
				#parse CITY, STATE y formatee según sea necesario; de lo   
				else:   
					city_region = city_region.lstrip('/l -').replace('-', '').split(',')   
					city ​​= city_region[0]   
					state_raw = city_region[1]   
					estado = ''
					    
					for char in region_raw:   
						if char.isupper():   
							estado + = char
							
					# Unir CIUDAD y ESTADO con cadenas abreviadas  
					location = city + ',' + region
					
					# Escribirlos en el archivo   
					f.write(location + '\n')
	#cerrar archivo   
	f.close ()
```

Ejecutando este código ahora debería existir un archivo de texto con todas las ciudades de Catalunya.

Ahora volvemos al archivo `indeed_scraper_api.py` y agregamos la función final.

```
def searchAllCities():

	# Contador del número de ciudades   
	current_city = 0
	
	# Abre el archivo de texto de ciudades   
	with open('cities', 'r', encoding ='UTF8') as myfile:
	
		# Obtiene todas las ciudades en una lista de   
		locations= myfile.read().split('\n')
		
	# Obtiene el número total de ciudades   
	city_number = len(locations)
	 
	# Recorre todas las ciudades  
	while current_city < city_number:   
	             
		# Define city search location   
		params['l'] = locations[current_city]   
		             
		# Ejecuta la función de búsqueda principal y obtiene las ofertas   
		get_offers(params)
		
		# Incrementa en uno el contador de ciudades 
		current_city += 1
```
 
Ahora solo se necesita ejecutar `searchAllCities()`y ver cómo la base de datos se llena de ofertas de trabajo :)

## **DJANGO, EL FRAMEWORK**

Creamos un proyecto en Django tal y como procede según la guía, es decir, preparamos nuestra máquina con todos los elementos que hacen falta para poder ejecutar el framework con robustez. Para ello instalamos una serie librerías, tanto de forma global como en el entorno virtual.

Las librerías que debemos instalar son: Obviamente *Python*, *PIP*, *Python3-venv* y *Django*, para trabajar con base de datos debemos elegir el SGDB de nuestra preferencia. Tenemos que tener en cuenta que Django cuenta con *SQLite3* como sistema integrado, pero tiene función nativa con *PostgreSQL*, y también funciona perfectamente con *MySQL*. Así, tendremos que instalar cualquiera de ellos y a su vez la pertinente librería para su funcionamiento bajo Python. Tenemos librerías como *Psycopg2* para PostgreSQL, *PyMySQL* o *MySQLClient* para MySQL.

Luego para nuestro proyecto, ya haciendo uso del entorno virtual: *Pillow* para el tratamiento de carga de archivos, por ejemplo imágenes, ...

Creamos una carpeta de proyecto con el nombre **TecnoJob**, tal y como pueda llamarse la app principal. Dentro creamos la estructura de directorios propia de Django de la que cabe destacar la propia de configuración, podríamos decir la vía de entrada desde donde se ejecuta el resto.  En esta se aloja un archivo llamado *settings.py* que deberemos configurar previamente para poder correr la app con toda garantía de funcionalidad. Otro archivo igualmente importante es *url.py*, donde introducimos la lista de direcciones url que conectarán las distintas partes de la app.

Al mismo nivel que este directorio de config, situamos otros 4 que asignamos como app, es importante diferenciarlas del proyecto, así organizaremos de forma natural la estructura del proyecto. A esas carpetas las llamaremos respectivamente: **auth**, donde alojaremos todo lo relacionado con la autenticación del usuario. Otra llamada **offer_crud**, donde crearemos la lógica de negocio entorno a las ofertas de empleo. Otra llamada **gencv_offer** donde haremos lo propio para la sección de generación de curriculums. Y finalmente, una llamada **api**, donde incluiremos todo lo que tiene que ver con el funcionamiento de la api de ofertas de empleo que nos suministrará los datos que necesitamos.

Al crear este nivel de estructura lo primero que tenemos que tener en cuenta es que cada carpeta de aplicación debe contener su propio archivo *url.py* en la que asociaremos las funciones o clases que contendrán a su vez otro archivo igualmente importante: *views.py*. El contenido del archivo url.py de cada app debe estar vinculado al archivo url.py de la carpeta de configuraciones, todo esto mediante la importación de la librería nativa de Django llamada *include*.
