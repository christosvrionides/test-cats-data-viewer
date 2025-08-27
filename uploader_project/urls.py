# uploader_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # ✅ CORRECTED: This now correctly points all root URLs to your viewer app
    path("", include("viewer.urls")),
    
    # If you are using OIDC, keep this line
    path('oidc/', include('mozilla_django_oidc.urls')),
]