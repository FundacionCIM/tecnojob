from django.shortcuts import redirect
from pages.views import *

import psycopg2
import psycopg2.extras


# Create your views here.
def company_view(request):
    if request.method == 'POST':
        conn = psycopg2.connect(dbname="tecnojob00", user="postgres", password="47601469W", host="localhost", port=5432)

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        name = request.POST.get("name", default=None)
        cif = request.POST.get("cif", default=None)
        email = request.POST.get("email", default=None)
        url = request.POST.get("url", default=None)

        insertSQL = "INSERT INTO company (c_name, cif, email, site) VALUES (%s, %s, %s, %s);"
        placeholder = (name, cif, email, url)

        cursor.execute(insertSQL, placeholder)
        # cursor.execute(f"insert into company (c_name, cif, email, site) values ({name}, {cif}, {email}, {url});")

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("mostrar_empresa")
    else:
        conn = psycopg2.connect(dbname="tecnojob00", user="postgres", password="47601469W", host="localhost", port=5432)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("SELECT * FROM company ORDER BY c_name;")

        empresas = cursor.fetchall()
        params = {"empresas": empresas}

        cursor.close()
        conn.close()

        return render(request, "company_create.html", params)


def company_delete(request, id):
    conn = psycopg2.connect(dbname="tecnojob00", user="postgres", password="47601469W", host="localhost", port=5432)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute(f"DELETE FROM company WHERE company_id={id}")

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("mostrar_empresa")


def company_update(request, id):
    conn = psycopg2.connect(dbname="tecnojob00", user="postgres", password="47601469W", host="localhost", port=5432)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    updateSQL = f"UPDATE company SET c_name=%s, cif=%s, email=%s, site=%s WHERE company_id={id};"
    placeholder = (
        request.POST.get("name", default=None),
        request.POST.get("cif", default=None),
        request.POST.get("email", default=None),
        request.POST.get("url", default=None)
    )

    cursor.execute(updateSQL, placeholder)

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("mostrar_empresa")
    # return render(request, "company_create.html")
