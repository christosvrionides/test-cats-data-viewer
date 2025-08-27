# viewer/views.py

import os
import yaml
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def view_datasets(request):
    """
    This view now scans the local 'data/' directory for .yaml files
    and passes them to the template to populate the dropdown.
    """
    data_dir = Path(settings.BASE_DIR) / 'data'
    datasets = []

    try:
        for filename in os.listdir(data_dir):
            if filename.endswith(('.yaml', '.yml')):
                with open(data_dir / filename, 'r') as f:
                    data = yaml.safe_load(f)
                    # Get the database name from the YAML content
                    db_name = data.get('owner_classification', {}).get('database_name', filename)
                    datasets.append({'file': filename, 'name': db_name})
    except FileNotFoundError:
        print("Error: The 'data' directory was not found in your project's root.")
    except Exception as e:
        print(f"An error occurred while reading YAML files: {e}")

    return render(request, "viewer/view_datasets.html", {"datasets": datasets})


@login_required
def get_dataset(request, dataset_name):
    """
    This view now reads a specific YAML file from the 'data/' directory
    and returns its content as a JSON response.
    """
    data_dir = Path(settings.BASE_DIR) / 'data'
    file_path = data_dir / dataset_name

    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return JsonResponse(data)
    except FileNotFoundError:
        return JsonResponse({"error": "Dataset not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)