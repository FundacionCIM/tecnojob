from django.shortcuts import render, redirect
from pages.views import *
from django.contrib import messages

import psycopg2
import psycopg2.extras


# Create your views here.
def cv_create(request):
    if request.method == 'POST':
        conn = psycopg2.connect(dbname="tecnojob00", user="postgres", password="47601469", host="localhost", port=5432)

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        edu_dates  = request.POST.getlist("edu_dates[]",  default=None)
        edu_school = request.POST.getlist("edu_school[]", default=None)
        edu_awards = request.POST.getlist("edu_awards[]", default=None)

        exp_dates     = request.POST.getlist("exp_dates[]",     default=None)
        exp_companies = request.POST.getlist("exp_companies[]", default=None)
        exp_position  = request.POST.getlist("exp_position[]",  default=None)

        course_dates = request.POST.getlist("course_dates[]", default=None)
        course_names = request.POST.getlist("course_names[]", default=None)
        course_info  = request.POST.getlist("course_info[]",  default=None)

        for  in edu_dates:
            cursor.execute("INSERT INTO cv (edu_dates) VALUES (%s);", (ed, ))

        for es in edu_school:
            cursor.execute("INSERT INTO cv (edu_school) VALUES (%s);", (es, ))

        for es in edu_school:
            cursor.execute("INSERT INTO cv (edu_school) VALUES (%s);", (es, ))






        # insertSQL = "INSERT INTO company (c_name, cif, email, site) VALUES (%s, %s, %s, %s);"
        # placeholder = (name, cif, email, url)
        #
        # cursor.execute(insertSQL, placeholder)
        # cursor.execute(f"insert into company (c_name, cif, email, site) values ({name}, {cif}, {email}, {url});")

        conn.commit()
        cursor.close()
        conn.close()

    return render(request, "cv_create.html")
