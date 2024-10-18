from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .utils import probe_model_5l_profit

def upload_file(request):
    if request.method == "POST":
        uploaded_file = request.FILES['data_file']
        data = json.load(uploaded_file)
        result = probe_model_5l_profit(data["data"])
        request.session['result'] = result  # Store result in session
        return redirect('result')  # Redirect to result page
    return render(request, 'upload.html')

def display_result(request):
    result = request.session.get('result', None)  # Get result from session
    if result is None:
        return redirect('upload')  # If no result, go back to upload page
    return render(request, 'result.html', {'result': result})