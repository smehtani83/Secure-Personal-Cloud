from django import forms
from .models import File, Enc , sharing_keys , rec , Id , Shared_File
from django.contrib.auth.models import User

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file_name', 'file_type', 'file_file','file_address','md5sum']

class ShareForm(forms.ModelForm):
    class Meta:
        model = Shared_File
        fields = ['file_name', 'file_type', 'file_file','file_address','md5sum' , 'userb']

class RemoveShareForm(forms.ModelForm):
    class Meta:
        model = Shared_File
        fields = ['file_name', 'file_type','file_address','md5sum' , 'userb']

class SearchForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file_name', 'file_type','file_address','md5sum']


class DeleteForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file_name', 'file_type','file_address']

class DownloadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file_name', 'file_type','file_address']

class Down(forms.ModelForm):
    class Meta:
        model = Id
        fields = ['usera']

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Enc
        fields = ['private_key', 'schema','shared_key']

class WebForm(forms.ModelForm):
    class Meta:
        model = Enc
        fields = ['private_key' , 'schema']
        
class GetKey(forms.ModelForm):
    class Meta:
        model = sharing_keys
        fields = ['n', 'e', 'd']

class GetA(forms.ModelForm):
    class Meta:
        model = Id
        fields = ['usera']

class GetB(forms.ModelForm):
    class Meta:
        model = Id
        fields = ['usera']

class RecForm(forms.ModelForm):
    class Meta:
        model = rec
        fields = ['usera', 'sofbwa', 'file']


#class SyncForm(forms.ModelForm):
 #   class Meta:
  #      model = Sync
   #     fields = ['dir_path']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

