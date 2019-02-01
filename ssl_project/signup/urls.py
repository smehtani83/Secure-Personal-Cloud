from django.conf.urls import include, url
from . import views

app_name = 'signup'

urlpatterns = [
    url(r'^$', views.SignUp.as_view(), name='signup'),
]