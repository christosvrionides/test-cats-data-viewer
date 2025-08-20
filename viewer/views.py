# viewer/views.py

import json
from django.http import JsonResponse
from django.shortcuts import render
from minio import Minio
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required
def view_datasets(request):
    """
    This view connects to Minio, gets a list of all .json files in the bucket,
    and passes them to the template to populate the dropdown.
    """
    try:
        # Establish a connection to the Minio server
        client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False  # Set to True if your Minio instance uses HTTPS
        )
        
        # List all objects in the bucket
        objects = client.list_objects(settings.MINIO_BUCKET_NAME, recursive=True)
        
        # Filter the list to include only files that end with .json
        datasets = [obj.object_name for obj in objects if obj.object_name.endswith('.json')]

    except Exception as e:
        # If there's an error (e.g., Minio is down), print it and return an empty list
        print(f"Error connecting to Minio: {e}")
        datasets = []

    # Render the HTML template, passing the list of dataset names to it
    return render(request, "viewer/view_datasets.html", {"datasets": datasets})

@login_required
def get_dataset(request, dataset_name):
    """
    This view acts as an API endpoint. The JavaScript on the frontend will call 
    this URL to get the contents of a specific .json file from Minio.
    """
    try:
        # Establish a connection to the Minio server
        client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False  # Set to True if your Minio instance uses HTTPS
        )

        # Get the specific object (file) from the bucket
        response = client.get_object(settings.MINIO_BUCKET_NAME, dataset_name)
        
        # Read the file's content and parse it as JSON
        data = json.loads(response.read())
        
        # Return the data as a JSON response
        return JsonResponse(data)

    except Exception as e:
        # If there's an error, return a JSON error message with a 500 status code
        return JsonResponse({"error": str(e)}, status=500)
