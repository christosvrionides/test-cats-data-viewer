# uploader/views.py

from django.contrib import messages
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.views import View

# This now imports from your new local oidc.py file
from .oidc import OIDCLoginRequiredMixin


class data_uploader_view(OIDCLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """Handles displaying the upload form page."""
        return render(request, 'uploader/data_uploader.html')

    def post(self, request, *args, **kwargs):
        """Handles the file upload submission."""
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