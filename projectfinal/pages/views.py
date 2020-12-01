from django.shortcuts import render, redirect
from pages.forms import FormularioPost
from django.contrib import messages
from django.db import connection
from pages.models import Post
from django.core.paginator import Paginator

from bs4 import BeautifulSoup
from urllib.request import urlopen
from careerjet_api import CareerjetAPIClient

import pymysql
import psycopg2
import psycopg2.extras


# import psycopg2.extras


# Función principal
def index(request):
    # listado_ofertas = Post.objects.all()
    # paginator = Paginator(listado_ofertas, 3)
    # pagina = request.GET.get("page") or 1
    # ofertas = paginator.get_page(pagina)
    # pagina_actual = int(pagina)
    # paginas = range(1, ofertas.paginator.num_pages + 1)

    keyword = request.POST.get("keyword", default=None)
    location = request.POST.get("location", default=None)
    offer_list_view = None

    if keyword is not None and location is not None:
        api_offer_list = get_offers_api(keyword, location)
        #db_offer_list = get_offers_db(keyword, location)

        save_to_db(request, api_offer_list)
        offer_list_view = api_offer_list
        #list_view = db_offer_list + api_offer_list
    print(offer_list_view)
    return render(request, "oferta_empleo.html", {"offer_list_view": offer_list_view})


# Función para obtener datos de la api
def get_offers_api(keyword, location):
    client = CareerjetAPIClient("es_ES")

    search_results = client.search({
        'location': location,
        'keywords': keyword,
        'sort': 'date',
        'pagesize': '100',
        # 'page': '5',
        'affid': '213e213hd12344552',
        'user_ip': '62.174.168.4',
        'url': 'http://www.example.com/jobsearch?q=dba&l=barcelona',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69 '
    })

    # Devolvemos la lista de resultados
    api_offer_list = []

    for elm in search_results['jobs']:
        offer = {
            "title": elm.get('title', None),
            "company": elm.get('company', None),
            "salary": elm.get('salary', None),
            "sal_min": elm.get('salary_min', None),
            "sal_max": elm.get('salary_max', None),
            "publi_date": elm.get('date', None),
            "description": elm.get('description', None),
            "url": elm.get('url', None),
            "site": elm.get('site', None)
        }
        api_offer_list.append(offer)

    return api_offer_list


# Función para obtener datos de la BD
def get_offers_db(keyword, location):
    db = psycopg2.connect(dbname="tecnojob00", user="postgres", password=47601469, host="localhost", port=5432)

    # preparar un objeto de cursor usando el método cursor()
    # cursor = db.cursor()
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        # Devolvemos la lista de resultados
        # db_offer_list = []

        cursor.execute("select * from oferta, provincia where oferta.nombre_ofrt = %s and provincia.nombre_prov %s", (keyword, location,))
        result = cursor.fetchall()
        return result
        # db_offer_list.append(result)
    except:
        # Revertir en caso de que haya algún error
        db.rollback()


# Guardar en BD
def save_to_db(request, api_offer_list):
    db = psycopg2.connect(dbname="tecnojob00", user="postgres", password=47601469, host="localhost", port=5432)

    # preparar un objeto de cursor usando el método cursor()
    cursor = db.cursor()
    # cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        for offer in api_offer_list:
            # Ejecutar procedimiento almacenado SQL
            cursor.execute(f"insert into oferta (nombre_ofrt, empr_id, cat_id) values ({offer[0]}, '1', '1');")

            # Hacer el commit a la base de datos
            db.commit()
            messages.success(request, f"La oferta se ha guardado correctamente.")
    except:
        # Revertir en caso de que haya algún error
        db.rollback()

    # # Usamos esta función para agregar ofertas a nuestra BBDD
    # with connection.cursor() as cursor:
    #     try:
    #         for offer in offer_list:
    #             # Ejecutar procedimiento almacenado MySQL
    #             # Ejecutar procedimiento almacenado MySQL
    #             cursor.execute(
    #                 "insert into empresa(nombre_empr, cif, email, site) values ('xibalba', 'W47601469', /"
    #                 "'info@xibalba.com', 'https://www.xibalba.com');")
    #             # cursor.execute(f"CALL sp_insert_data({offer[0]}, )")
    #             row = cursor.fetchone()
    #             # Hacemos el commit a la base de datos
    #             connection.commit()
    #         return row
    #     except:
    #         # Revertir en caso de que haya algún error
    #         connection.rollback()
#
# def index(request):
#     # return HttpResponse('Hola bienvenid@ a TecnoJob')
#     return render(request, "searcher.html")


# def offer_insert(request):
#     conn = psycopg2.connect(dbname="tecnojob00", user="postgres", password="47601469W", host="localhost", port=5432)
#     cursor = conn.cursor()
#     cursor.execute("insert into offer (title, salary, remote, publi_date, company_id, cat_id) values (%s, %s, %s, %s, %s, %s);", ('DBA', 10000, True, '2020-11-28', 4, 1))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return HttpResponse('Registro Insertado')
#     # return render(request, "offer_create.html")
#
#
# def offer_select(request):
#     conn = psycopg2.connect(dbname="tecnojob00", user="postgres", password="47601469W", host="localhost", port=5432)
#     cursor = conn.cursor()
#     cursor.execute("select * from offer;")
#     return HttpResponse(cursor.fetchall())
#     # return render(request, "offer_read.html")
#
#
# def offer_update(request):
#     conn = psycopg2.connect(dbname="tecnojob00", user="postgres", password="47601469W", host="localhost", port=5432)
#     return render(request, "offer_update.html")
#
#
# def offer_delete(request):
#     conn = psycopg2.connect(dbname="tecnojob00", user="postgres", password="47601469W", host="localhost", port=5432)
#     return render(request, "offer_delete.html")


def crear_oferta(request):
    try:
        with connection.cursor() as cursor:
            # Ejecutar procedimiento almacenado MySQL
            cursor.execute("insert into oferta(nombre_ofrt, descrip, salario, sal_min, sal_max, tcontr, periodo,  /"
                           "remote, url, site, fecha_publi, empr_id, cat_id) values('dba', '21000', '20000', '25000', /"
                           "'media jornada', 'fin servicio', 'False', 'https://www.google.es', 'www.google.es', /"
                           "'2020/07/12', '1', '1');")
            row = cursor.fetchone()
            # Hacemos el commit a la base de datos
            connection.commit()

        return row
    except:
        # Revertir en caso de que haya algún error
        connection.rollback()


def crear_empresa(request, company_list):
    try:
        with connection.cursor() as cursor:
            # Ejecutar procedimiento almacenado MySQL
            cursor.execute("insert into empresa(nombre_empr, cif, email, site) values ('xibalba', 'W47601469', /"
                           "'info@xibalba.com', 'https://www.xibalba.com');")
            row = cursor.fetchone()
            # Hacemos el commit a la base de datos
            connection.commit()
        return row
    except:
        # Revertir en caso de que haya algún error
        connection.rollback()


def crear_categoria(request, cat_list):
    try:
        with connection.cursor() as cursor:
            # Ejecutar procedimiento almacenado MySQL
            cursor.execute("insert into categoria (nombre_cat) values ('Base de datos');")
            row = cursor.fetchone()
            # Hacemos el commit a la base de datos
            connection.commit()
        return row
    except:
        # Revertir en caso de que haya algún error
        connection.rollback()


def crear_post(request):
    if request.method == "POST":
        form = FormularioPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor_id = request.user.id
            post.save()
            titulo = form.cleaned_data.get("titulo")
            messages.success(request, f"La oferta {titulo} se ha creado correctamente")
            return redirect("oferta")
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])

    form = FormularioPost()
    return render(request, "crear_oferta.html", {"form": form})


def crear_cv(request):
    pass


def eliminar_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        messages.error(request, 'La publicación que quieres eliminar no existe.')
        return redirect("blog")

    if post.autor != request.user:
        messages.error(request, 'No eres el autor de esta publicación.')
        return redirect("blog")

    post.delete()
    messages.success(request, f"El post {post.titulo} ha sido eliminado!")
    return redirect("blog")

# if __name__ == '__main__':
#     res = get_offers('es_ES')
#     for offer in res:
#         print(offer[0])


# Definimos las variables para nuestras fuentes de URL
# BASE_URL = "https://www.opcionempleo.com/"
# regions_URL = "https://www.opcionempleo.com/ofertas-empleo-provincia-de-barcelona-34873.html"

# Las listas que contendrán nuestras comarcas y ciudades
# region_URL_list = []
# cities_name_list = []

# Nuestra función para buscar y crear la lista de comarcas
# def getRegionLinks(regions_URL):
# Obtener la fuente de la página URL de comarcas
# html = urlopen(regions_URL).read()

# Crear el objeto BeautifulSoup
# soup = BeautifulSoup(html, "lxml")

# Usamos un método Bs para encontrar la sección de enlaces
# region_page = soup.find_all()

# Luego un bucle para obtener los enlaces de todos las comarcas
# y construimos cada enlace de lsa comarcas usando los relativos
# for cities in region_page:
#     links = cities.findAll('a')
#     for a in links:
#         if a.text != '':
#             region_URL_list.append(BASE_URL + a['href'])

# finalmente devolvemos la lista de URL de las comarcas
# return region_URL_list

# url = 'https://www.opcionempleo.com/ofertas-empleo-provincia-de-barcelona-34873.html'
# page = requests.get(url)
# soup = BeautifulSoup(page.content, 'html.parser')
#
# ciud = soup.find('a', a_attr='Granollers, Barcelona')
#
# print(ciud)
