from django.contrib import admin
from .models import File, Enc, sharing_keys,rec,Shared_File

admin.site.register(File)
admin.site.register(Enc)
admin.site.register(sharing_keys)
admin.site.register(rec)
admin.site.register(Shared_File)
# Register your models here.
