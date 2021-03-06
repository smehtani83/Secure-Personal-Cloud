from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    fullname = forms.CharField(label = "Full name")
    class Meta:
        model = User
        fields = ("username", "fullname", "email", )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        first_name, last_name = self.cleaned_data["fullname"].split()
        user.first_name = first_name
        user.last_name = last_name
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class SignUp(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'