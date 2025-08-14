# uploader/views.py

from django.contrib import messages
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from mozilla_django_oidc.auth import oidc_login_required

@oidc_login_required
def data_uploader_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file-upload')

        if not uploaded_file or not uploaded_file.name.lower().endswith('.csv'):
            messages.error(request, "Please select a valid CSV file to upload.")
            return redirect('data_uploader')

        try:
            saved_path = default_storage.save(uploaded_file.name, uploaded_file)
            messages.success(request, f"Successfully uploaded '{saved_path}' to your bucket.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")

        return redirect('data_uploader')

    return render(request, 'uploader/data_uploader.html')