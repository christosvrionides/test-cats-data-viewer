# uploader/views.py

from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.module_loading import import_string
from django.views import View
from django.core.files.base import ContentFile
import json
import os

# This now imports from your new local oidc.py file
from .oidc import OIDCLoginRequiredMixin


class data_uploader_view(OIDCLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """Handles displaying the upload form page."""
        return render(request, 'uploader/data_uploader.html')

    def post(self, request, *args, **kwargs):
        """Handles the file upload and metadata submission."""
        uploaded_file = request.FILES.get('file-upload')
        metadata_json = request.POST.get('metadata_json')

        if not uploaded_file or not uploaded_file.name.lower().endswith('.csv'):
            messages.error(request, "Please select a valid CSV file to upload.")
            return redirect('data_uploader')

        try:
            # Dynamically load the storage class from your settings
            StorageClass = import_string(settings.STORAGES['default']['BACKEND'])
            storage = StorageClass()
            
            # First, save the main CSV file
            csv_path = storage.save(uploaded_file.name, uploaded_file)
            messages.success(request, f"Successfully uploaded '{csv_path}' to your bucket.")

            # Now, handle the metadata by saving it as a separate JSON file
            if metadata_json and metadata_json != '[]':
                try:
                    # Define a path for the metadata file, based on the CSV's path
                    base_path, _ = os.path.splitext(csv_path)
                    metadata_path = f"{base_path}.metadata.json"

                    # Convert the JSON string to bytes and create a Django ContentFile
                    metadata_content = ContentFile(metadata_json.encode('utf-8'))

                    # Save the metadata file to MinIO
                    storage.save(metadata_path, metadata_content)
                    messages.success(request, f"Successfully saved metadata to '{metadata_path}'.")

                except Exception as e:
                    # If metadata saving fails, we should ideally delete the original CSV
                    # to avoid orphaned files. For now, we'll just show an error.
                    storage.delete(csv_path) # Attempt to clean up
                    messages.error(request, f"Uploaded CSV '{csv_path}' but failed to save metadata. The upload has been rolled back. Error: {e}")
                    return redirect('data_uploader')

        except Exception as e:
            messages.error(request, f"An unexpected error occurred during file upload: {e}")

        return redirect('data_uploader')