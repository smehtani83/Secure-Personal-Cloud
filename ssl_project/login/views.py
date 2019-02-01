from django.shortcuts import render, get_object_or_404 , render_to_response
from .forms import FileForm, UserForm , SearchForm, DeleteForm, DownloadForm, RegisterForm , GetKey , RecForm , GetA, GetB , ShareForm, RemoveShareForm , Down, WebForm
from .models import File, Enc , sharing_keys , rec , Shared_File
import sqlite3 as lite
from pathlib import Path
import hashlib
import os
from django.contrib.auth import logout
import base64
from django.http import JsonResponse
from django.http import HttpResponse
import json
#def create_path(request):
 #   if not request.user.is_authenticated():
  #      return render(request, 'home.html')
   # else:
    #    form = SyncForm(request.POST or None)
     #   if form.is_valid():
      #      file = form.save(commit=False)
       #     file.user = request.user
        #    file.dir_path = form.cleaned_data.get("path")
         #   file.save()
        #context = {
         #   'form': form,
          #  'user': request.user,
           # 'error_message': 'path added successfully'
        #}
        #return render(request, 'login/file_form.html', context)


def create_file(request):
    if not request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        form = FileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            name = form.cleaned_data.get("file_name")
            file.file_type = form.cleaned_data.get("file_type")
            file.md5sum = form.cleaned_data.get("md5sum")
            ad = form.cleaned_data.get("file_file")
            file.file_name = "delete123456789"
            #data = request.FILES['file_file']
            file.file_address = form.cleaned_data.get("file_address")
            file.save()
            a = '/ssl_project/media/' + str(ad)
            home = str(Path.home())
            a = home + a
            fl = open('%s' %a,'rb')
            data=None
            with fl:
                data = fl.read()
            a = home + '/ssl_project/db.sqlite3'
            con = lite.connect('%s' %a)
            with con:
                cur = con.cursor()
                sql = "INSERT INTO LOGIN_FILE(FILE_FILE, USER_ID, FILE_NAME, FILE_TYPE, FILE_ADDRESS, MD5SUM) VALUES (?,?,?,?,?,?)"
                cur.execute(sql, (lite.Binary(data), request.user.id, name, file.file_type, file.file_address, file.md5sum))
            File.objects.filter(file_name="delete123456789").delete()
                #cur.execute("DELETE FROM LOGIN_FILE where FILE_FILE = (?) & USER_ID = (?) & FILE_NAME + (?) & FILE_TYPE = (?)",(file.file_file, request.user.id, file.file_name, file.file_type))
            #os.remove('%s' %a)
        context = {
            'form' : form,
            'user' : request.user,
            'error_message': 'File Uploaded Successfully'
        }
        return render(request, 'login/file_form.html', context)

def create_search(request):
    if not request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        form = SearchForm(request.POST or None)
        a = []
        b = []
        if form.is_valid():
            user = request.user
            file_name = form.cleaned_data.get("file_name")
            file_type = form.cleaned_data.get("file_type")
            file_address = form.cleaned_data.get("file_address")
            md5sum = form.cleaned_data.get("md5sum")
            a = File.objects.filter(file_name=file_name,file_type=file_type,file_address=file_address,user_id=request.user.id)
            b = File.objects.filter(file_name=file_name, file_type=file_type, file_address=file_address,user_id=request.user.id,md5sum=md5sum)
        if len(a)==0:
            context = {
                'form': form,
                'user': request.user,
                'error_message': 'no'
            }
            bool = 0
            return render(request, 'login/search_form.html', context)
        else:
            if len(b)==0:
                context = {
                    'form': form,
                    'user': request.user,
                    'error_message': 'yes'
                }
                return render(request, 'login/search_form.html', context)
            else:
                context = {
                    'form': form,
                    'user': request.user,
                    'error_message': 'np'
                }
                return render(request, 'login/search_form.html', context)

def create_delete(request):
    if not request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        form = DeleteForm(request.POST or None)
        if form.is_valid():
            user = request.user
            file_name = form.cleaned_data.get("file_name")
            file_type = form.cleaned_data.get("file_type")
            file_address = form.cleaned_data.get("file_address")
            File.objects.filter(file_name=file_name,file_type=file_type,file_address=file_address,user_id=request.user.id).delete()
        context = {
            'form': form,
            'user': request.user,
            'error_message': 'yes'
        }
        return render(request, 'login/delete_form.html', context)


def create_download(request):
    if not request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        form = DownloadForm(request.POST or None)
        if form.is_valid():
            user = request.user
            file_name = form.cleaned_data.get("file_name")
            file_type = form.cleaned_data.get("file_type")
            file_address = form.cleaned_data.get("file_address")
            blob = File.objects.filter(file_name=file_name,file_type=file_type,file_address=file_address,user_id=request.user.id)
            b = {
                "files": [
                    {
                        "blob" : str(blob[0].file_file),
                        "name" : str(blob[0].file_name),
                        "type" : str(blob[0].file_type),
                        "address": str(blob[0].file_address),

                    }
                ]
            }
            return render_to_response("login/data.html", b)
        context = {
            'form': form,
            'user': request.user,
            'error_message': "hi"
        }

        return render(request, 'login/download_form.html',context)

def data(request):
    return render(request, 'login/data.html', {})

def register(request):
    if not request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        form = RegisterForm(request.POST or None)
        a = []
        b = []
        if form.is_valid():
            enc = form.save(commit=False)
            enc.user = request.user
            enc.private_key = form.cleaned_data.get("private_key")
            enc.schema = form.cleaned_data.get("schema")
            enc.shared_key = form.cleaned_data.get("shared_key")
            b = Enc.objects.filter(user_id=request.user.id)
            a = Enc.objects.filter(user_id=request.user.id, private_key=enc.private_key, schema=enc.schema,shared_key=enc.shared_key)
            if len(b)==0:
                context = {
                    'form': form,
                    'user': request.user,
                    'error_message': 'abc'
                }
                enc.save()
                return render(request, 'login/register_form.html', context)
            else:
                if len(a) == 0:
                    context = {
                        'form': form,
                        'user': request.user,
                        'error_message': 'yes'
                    }

                    return render(request, 'login/register_form.html', context)
                else:
                    context = {
                        'form': form,
                        'user': request.user,
                        'error_message': 'no'
                    }
                    return render(request, 'login/register_form.html', context)
        context = {
            'form': form,
            'user': request.user,
            'error_message': 'no'
        }
        return render(request, 'login/register_form.html', context)


def download_json(request):
    if not request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        user = request.user
        blob = File.objects.filter(user_id=request.user.id)
        b = {
             "xyz" : {
                 "files": [

            ]
             }
        }
        for x in blob:
            dic = {
                    "blob" : base64.b64encode(x.file_file),
                    "name" : str(x.file_name),
                    "type" : str(x.file_type),
                    "address": str(x.file_address),

                }
            b["xyz"]["files"].append(dic)
        return render_to_response("login/data.json", b)

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'home.html', context)

def user_keys(request):
    if not request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        form = GetKey(request.POST or None)
        if form.is_valid():
            key = form.save(commit=False)
            key.user = request.user
            key.n = form.cleaned_data.get("n")
            key.e = form.cleaned_data.get("e")
            key.d = form.cleaned_data.get("d")
            key.save()
        context = {
            'form' : form,
            'user' : request.user,
            'error_message': 'yes'
        }
        return render(request, 'login/key_form.html', context)

def create_rec(request):
    if not request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        form = RecForm(request.POST or None)
        if form.is_valid():
            key = form.save(commit=False)
            key.userb = request.user
            key.usera = form.cleaned_data.get("usera")
            key.sofbwa = form.cleaned_data.get("sofbwa")
            key.file = form.cleaned_data.get("file")
            key.save()
        context = {
            'form' : form,
            'user' : request.user,
            'error_message': 'yes'
        }
        return render(request, 'login/rec_form.html', context)

def geta(request):
    if not request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        form = GetA(request.POST or None)
        st = " "
        if form.is_valid():
            a_id = int(form.cleaned_data.get("usera"))
            a = sharing_keys.objects.filter(user_id=a_id)
            n = a[0].n
            e = a[0].e
            st = "lol1234567890" + n + "lol0987654321" + e + "end1234567890"
        context = {
            'form' : form,
            'user' : request.user,
            'error_message': st
        }
        return render(request, 'login/key_detail.html', context)

def d_a(request):
    if not request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        st = " "
        a_id = request.user
        a = sharing_keys.objects.filter(user_id=a_id.id)
        d = a[0].d
        n = a[0].n
        st = "lol1234567890" + d + "lol0987654321" + n + "end1234567890"
        context = {
            'user' : request.user,
            'error_message': st
        }
        return render(request, 'login/dkey_detail.html', context)

def m_b(request):
    if not request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        form = GetB(request.POST or None)
        st = " "
        if form.is_valid():
            b = form.cleaned_data.get("usera")
            a = rec.objects.filter(usera=request.user.id,userb_id=b)
            userb = a[0].userb.id
            file = a[0].file
            sofbwa = a[0].sofbwa
            st = "lol1234567890" + str(userb) + "lol0987654321" + str(file) + "end1234567890" + str(sofbwa) + "newend3456789012"
        context = {
            'form' : form,
            'user' : request.user,
            'error_message': st,
        }
        return render(request, 'login/dkey1_detail.html', context)

def share_file(request):
    if not request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        form = ShareForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            file = form.save(commit=False)
            file.usera = request.user.id
            name = form.cleaned_data.get("file_name")
            file.file_type = form.cleaned_data.get("file_type")
            file.md5sum = form.cleaned_data.get("md5sum")
            file.userb = form.cleaned_data.get("userb")
            ad = form.cleaned_data.get("file_file")
            file.file_name = "delete123456789"
            #data = request.FILES['file_file']
            file.file_address = form.cleaned_data.get("file_address")
            file.save()
            a = '/ssl_project/media/' + str(ad)
            home = str(Path.home())
            a = home + a
            fl = open('%s' %a,'rb')
            data=None
            with fl:
                data = fl.read()
            a = home + '/ssl_project/db.sqlite3'
            con = lite.connect('%s' %a)
            with con:
                cur = con.cursor()
                sql = "INSERT INTO LOGIN_SHARED_FILE(FILE_FILE, USERA, FILE_NAME, FILE_TYPE, FILE_ADDRESS, MD5SUM,USERB) VALUES (?,?,?,?,?,?,?)"
                cur.execute(sql, (lite.Binary(data), file.usera, name, file.file_type, file.file_address, file.md5sum,file.userb))
            Shared_File.objects.filter(file_name="delete123456789").delete()
                #cur.execute("DELETE FROM LOGIN_FILE where FILE_FILE = (?) & USER_ID = (?) & FILE_NAME + (?) & FILE_TYPE = (?)",(file.file_file, request.user.id, file.file_name, file.file_type))
            #os.remove('%s' %a)
        context = {
            'form' : form,
            'user' : request.user,
            'error_message': 'File Uploaded Successfully'
        }
        return render(request, 'login/sharefile_form.html', context)

def share_remove(request):
    if not request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        form = RemoveShareForm(request.POST or None)
        if form.is_valid():
            file = form.save(commit=False)
            file.usera = request.user.id
            file.name = form.cleaned_data.get("file_name")
            file.file_type = form.cleaned_data.get("file_type")
            file.md5sum = form.cleaned_data.get("md5sum")
            file.userb = form.cleaned_data.get("userb")
            Shared_File.objects.filter(file_name=file.name,usera=file.usera,userb=file.userb,file_type=file.file_type,md5sum=file.md5sum).delete()
                #cur.execute("DELETE FROM LOGIN_FILE where FILE_FILE = (?) & USER_ID = (?) & FILE_NAME + (?) & FILE_TYPE = (?)",(file.file_file, request.user.id, file.file_name, file.file_type))
            #os.remove('%s' %a)
        context = {
            'form' : form,
            'user' : request.user,
            'error_message': 'File Uploaded Successfully'
        }
        return render(request, 'login/removefile_form.html', context)


def down(request):
    if not request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        userb = request.user.id
        blob = Shared_File.objects.filter(userb=userb)
        b = {
             "xyz" : {
                 "files": [
           ]
            }
        }
        for x in blob:
            dic = {
                    "blob" : base64.b64encode(x.file_file),
                    "name" : str(x.file_name),
                    "type" : str(x.file_type),
                    "address": str(x.file_address),

                }
            b["xyz"]["files"].append(dic)
        return render_to_response("login/share_data.json", b)



def base64res(request):
    blob = File.objects.filter(user_id=request.user.id)
    for x in blob:
        dic = {
            "blob": base64.b64encode(x.file_file),
            "name": str(x.file_name),
            "type": str(x.file_type),
            "address": str(x.file_address),
        }
        b["xyz"]["files"].append(dic)
    return JsonResponse(data)

def openwin(request):
    uid=int(request.POST.get('uid'))
    serial = int(request.POST.get('fid'))
    #uid = 1
    files = File.objects.filter(user_id=uid,id=serial)

    data = str(files[0].file_file)
    #data1 = str(data[2:-1])
    data1=str(base64.b64encode(files[0].file_file))
    exten = str(files[0].file_type)
    return render(request, 'render.html', {'data': data1, 'ext': exten})

