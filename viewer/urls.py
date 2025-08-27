# viewer/urls.py

from django.urls import path
from . import views

app_name = 'viewer'

urlpatterns = [
    # This will be the main page for the viewer app, at the root URL ("/")
    path('', views.view_datasets, name='view_datasets'),
    
    # This is the API endpoint for fetching dataset details
    path('get_dataset/<str:dataset_name>/', views.get_dataset, name='get_dataset'),
]