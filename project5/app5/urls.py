from django.conf.urls import url
from . import views


app_name = 'app5'

urlpatterns = [
    
    url(r'^help/$', views.help, name = "help")
]
