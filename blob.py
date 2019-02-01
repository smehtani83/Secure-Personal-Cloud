import sqlite3 as lite

fl = open('me.html', 'rb')

with fl:
    data = fl.read()

con = lite.connect('test.db')

with con:

    cur = con.cursor()     

    cur.execute("CREATE TABLE IF NOT EXISTS Docs(Data BLOB)")

    sql = "INSERT INTO Docs(Data) VALUES (?)" 
    cur.execute(sql, (lite.Binary(data), ))


from django.contrib.auth import logout
def create_file(request):
    if not request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        form = FileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            file.file_name = form.cleaned_data.get("file_name")
            file.file_type = form.cleaned_data.get("file_type")
            ad = form.cleaned_data.get("file_file")
            data = request.FILES['file_file']
            a = '/ssl_project/media/' + str(ad)
            home = str(Path.home())
            a = home + a
            fl = open('%s' %a,'rb')
            with fl:
                data = fl.read()
            a = home + '/ssl_project/db.sqlite3'
            con = lite.connect('%s' %a)
            with con:
                cur = con.cursor()
                sql = "INSERT INTO LOGIN_FILE(FILE_FILE, USER_ID, FILE_NAME, FILE_TYPE) VALUES (?,?,?,?)"
                cur.execute(sql, (lite.Binary(data), request.user.id, file.file_name, file.file_type))
            #os.remove('%s' %a)
        context = {
            'form' : form,
            'user' : request.user,
        }
        return render(request, 'login/file_form.html', context)
