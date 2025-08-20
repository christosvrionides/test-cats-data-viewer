# viewer/urls.py

from django.urls import path
from . import views

# This list defines the URL patterns for the viewer app.
urlpatterns = [
    # The root path "" will map to the `view_datasets` function in views.py.
    # This will be the main page of your viewer app.
    path("", views.view_datasets, name="view_datasets"),

    # This path is for the API endpoint that the JavaScript will call.
    # It captures the dataset_name from the URL and passes it to the `get_dataset` view.
    path("get_dataset/<path:dataset_name>/", views.get_dataset, name="get_dataset"),
]
