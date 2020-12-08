from django.shortcuts import redirect
# from django.contrib import messages
#
# import psycopg2
# import psycopg2.extras
#
#
# # Create your views here.
# def candidate_view(request):
#     if request.method == 'POST':
#
#         conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
#         cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#
#         candidate_view = request.POST.get("prov_name", default=None)
#
#         address  = request.POST.get("address",  default=None)
#         dni   = request.POST.get("dni",   default=None)
#         telephone = request.POST.get("telephone", default=None)
#         mobile   = request.POST.get("mobile",   default=None)
#         nacionalidad = request.POST.get("nacionalidad", default=None)
#         residencia = request.POST.get("residencia", default=None)
#         birth_date = request.POST.get("birth_date", default=None)
#
#         insertSQL = "INSERT INTO candidate (c_name) VALUES (%s);"
#      #   getData = (candidate_name, )
#
#      #   cursor.execute(insertSQL, getData)
#
#         conn.commit()
#         cursor.close()
#         conn.close()
#
#         messages.success(request, "El registro se ha guardado correctamente")
#         return redirect("mostrar_empresa")
#
#     else:
#
#         return render(request, "candidate_create.html", candidate_select())
#
#
# def candidate_select():
#     conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#
#     cursor.execute("SELECT * FROM candidate ORDER BY c_name;")
#
#     candidate = cursor.fetchall()
#     params = {"candidatos": candidate}
#
#     cursor.close()
#     conn.close()
#
#     return params
#
#
# def candidate_delete(request, id):
#     conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#
#     cursor.execute(f"DELETE FROM company WHERE candidate_id=%s", (id,))
#
#     conn.commit()
#     cursor.close()
#     conn.close()
#
#     messages.success(request, "El registro se ha borrado correctamente")
#     return redirect("mostrar_candidato")
#
#
# def transition_update(request, id):
#     conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#
#     cursor.execute(f"SELECT * FROM candidate WHERE candidate_id = %s", (id,))
#
#     empresas = cursor.fetchall()
#     params = {"empresas": empresas,
#               "id_empresa": id}
#
#     conn.commit()
#     cursor.close()
#     conn.close()
#
#     return render(request, "candidate_update.html", params)
#
#
# def candidate_update(request, id):
#     conn = psycopg2.connect(dbname="remotejob", user="postgres", password="3640", host="localhost", port=5432)
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#
#     updateSQL = f"UPDATE candidate SET c_name=%s, cif=%s, email=%s, site=%s WHERE company_id={id};"
#     getData = (
#         request.POST.get("name",  default=None),
#         request.POST.get("cif",   default=None),
#         request.POST.get("email", default=None),
#         request.POST.get("url",   default=None)
#     )
#
#     cursor.execute(updateSQL, getData)
#
#     conn.commit()
#     cursor.close()
#     conn.close()
#
#     return redirect("mostrar_empresa")
#     return render(request, "candidate_create.html")