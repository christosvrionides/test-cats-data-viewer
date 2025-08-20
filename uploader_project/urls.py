# uploader_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # This line tells Django that any request to the root URL ("/")
    # should be handled by the URL patterns defined in `viewer.urls`.
    path("", include("viewer.urls")),
    
    # This includes the necessary URLs for OIDC authentication.
    path('oidc/', include('mozilla_django_oidc.urls')),
]
