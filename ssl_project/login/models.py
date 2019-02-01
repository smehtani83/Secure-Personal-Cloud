from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import base64
class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    #file_link = models.CharField(max_length=500)
    file_name = models.CharField(max_length=100)
    file_file = models.FileField()
    file_address = models.CharField(max_length=1000)
    md5sum = models.CharField(max_length=100)
    def __str__(self):
#        return str(base64.b64encode(self.file_file))
        return str(self.file_name +" "+ self.file_type+" "+self.file_address)
    def acfile(self):
        return self.file_file
        
class Shared_File(models.Model):
    usera = models.IntegerField()
    userb = models.IntegerField()
    file_type = models.CharField(max_length=10)
    # file_link = models.CharField(max_length=500)
    file_name = models.CharField(max_length=100)
    file_file = models.FileField()
    file_address = models.CharField(max_length=1000)
    md5sum = models.CharField(max_length=100)

    def __str__(self):
        return str(self.file_name)
    def acfile(self):
        return self.file_file
#class Sync(models.Model):
 #   user = models.ForeignKey(User, on_delete=models.CASCADE)
  #  dir_path = models.CharField(max_length=500)
class lock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Enc(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    private_key = models.CharField(max_length=100)
    schema = models.CharField(max_length=100)
    shared_key = models.CharField(max_length=100)

class sharing_keys(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    n = models.CharField(max_length=1000)
    e = models.CharField(max_length=1000)
    d = models.CharField(max_length=1000)

class rec(models.Model):
    userb = models.ForeignKey(User, on_delete=models.CASCADE)
    usera = models.CharField(max_length=100)
    sofbwa = models.CharField(max_length=1000)
    file = models.CharField(max_length=100)

class Id(models.Model):
    usera = models.IntegerField()
