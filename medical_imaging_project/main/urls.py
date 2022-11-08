# main/urls.py

from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('show_img', views.show_img, name='show_img')
]