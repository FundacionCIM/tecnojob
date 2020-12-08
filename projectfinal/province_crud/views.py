from django.shortcuts import redirect, render
from django.contrib import messages

import psycopg2
import psycopg2.extras


# Create your views here.
def province_view(request):
    if request.method == 'POST':

        conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        prov_name = request.POST.get("prov_name",  default=None)

        insertSQL = "INSERT INTO province (p_name) VALUES (%s);"
        getData = (prov_name, )

        cursor.execute(insertSQL, getData)

        conn.commit()
        cursor.close()
        conn.close()

        messages.success(request, "El registro se ha guardado correctamente")
        return redirect("mostrar_provincia")

    else:

        return render(request, "province_create.html", province_select())


def province_select():
    conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("SELECT * FROM province ORDER BY p_name;")

    provincias = cursor.fetchall()
    params = {"provincias": provincias}

    cursor.close()
    conn.close()

    return params


def province_delete(request, id):
    conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute(f"DELETE FROM province WHERE prov_id=%s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    messages.success(request, "El registro se ha borrado correctamente")
    return redirect("mostrar_empresa")


def p_transition_update(request, id):
    conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute(f"SELECT * FROM province WHERE prov_id = %s", (id,))

    provincias = cursor.fetchall()
    params = {
        "provincias": provincias,
        "prov_id": id
    }

    conn.commit()
    cursor.close()
    conn.close()

    return render(request, "province_update.html", params)


def province_update(request, id):

    conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    updateSQL = f"UPDATE company SET p_name=%s WHERE prov_id={id};"
    getData = (
        request.POST.get("p_name",  default=None)
    )

    cursor.execute(updateSQL, getData)

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("mostrar_provincia")
    # return render(request, "company_create.html")