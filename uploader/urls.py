# uploader/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # This must use .as_view() because we are now using a class
    path('', views.data_uploader_view.as_view(), name='data_uploader'),
]