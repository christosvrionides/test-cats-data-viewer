# uploader_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("viewer.urls")),  # This will be the main page now
    path('oidc/', include('mozilla_django_oidc.urls')),
]