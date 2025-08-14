# uploader/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.data_uploader_view, name='data_uploader'),
]