from django.shortcuts import redirect, render
from django.contrib import messages

import psycopg2
import psycopg2.extras


# Create your views here.
def company_view(request):
    if request.method == 'POST':
        conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        name  = request.POST.get("name",  default=None)
        cif   = request.POST.get("cif",   default=None)
        email = request.POST.get("email", default=None)
        url   = request.POST.get("url",   default=None)

        insertSQL = "INSERT INTO company (c_name, cif, email, site) VALUES (%s, %s, %s, %s);"
        placeholder = (name, cif, email, url)

        cursor.execute(insertSQL, placeholder)
        # cursor.execute(f"insert into company (c_name, cif, email, site) values ({name}, {cif}, {email}, {url});")

        conn.commit()
        cursor.close()
        conn.close()

        messages.success(request, "El registro se ha guardado correctamente")
        return redirect("mostrar_empresa")
    else:
        return render(request, "company_create.html", company_select())


def company_select():
    conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("SELECT * FROM company ORDER BY c_name;")

    empresas = cursor.fetchall()
    params = {"empresas": empresas}

    cursor.close()
    conn.close()

    return params


def company_delete(request, id):
    conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute(f"DELETE FROM company WHERE company_id=%s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    messages.success(request, "El registro se ha borrado correctamente")
    return redirect("mostrar_empresa")


def transition_update(request, id):
    conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute(f"SELECT * FROM company WHERE company_id = %s", (id,))

    empresas = cursor.fetchall()
    params = {
        "empresas": empresas,
        "id_empresa": id
    }

    conn.commit()
    cursor.close()
    conn.close()

    return render(request, "company_update.html", params)


def company_update(request, id):
    conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    updateSQL = f"UPDATE company SET c_name=%s, cif=%s, email=%s, site=%s WHERE company_id={id};"
    getData = (
        request.POST.get("name",  default=None),
        request.POST.get("cif",   default=None),
        request.POST.get("email", default=None),
        request.POST.get("url",   default=None)
    )

    cursor.execute(updateSQL, getData)

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("mostrar_empresa")
    # return render(request, "company_create.html")
