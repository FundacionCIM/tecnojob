from django.shortcuts import redirect, render
from django.contrib import messages

import psycopg2
import psycopg2.extras


# Create your views here.
def city_view(request):
    if request.method == 'POST':
        conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        city_name = request.POST.get("city_name", default=None)

        insertSQL = "INSERT INTO city (city_name) VALUES (%s);"
        getData = (city_name, )

        cursor.execute(insertSQL, getData)

        conn.commit()
        cursor.close()
        conn.close()

        messages.success(request, "El registro se ha guardado correctamente")
        return redirect("mostrar_cuidad")
    else:
        return render(request, "city_create.html", city_select())


def city_select():
    conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("SELECT * FROM city ORDER BY city_name;")

    city = cursor.fetchall()
    params = {"ciudad": city}

    cursor.close()
    conn.close()

    return params


def city_delete(request, id):
    conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute(f"DELETE FROM city WHERE city_id=%s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    messages.success(request, "El registro se ha borrado correctamente")
    return redirect("mostrar_ciudad")


def c_transition_update(request, id):
    conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute(f"SELECT * FROM city WHERE city_id = %s", (id,))

    empresas = cursor.fetchall()
    params = {
        "ciudad": empresas,
        "ciudad_id": id
    }

    conn.commit()
    cursor.close()
    conn.close()

    return render(request, "city_update.html", params)


def city_update(request, id):
    conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    updateSQL = f"UPDATE company SET city_name=%s WHERE company_id={id};"
    getData = (
        request.POST.get("city_name",  default=None),
    )

    cursor.execute(updateSQL, getData)

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("mostrar_ciudad")
    #return render(request, "city_create.html")