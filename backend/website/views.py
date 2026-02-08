# backend\website\views.py
from django.http import JsonResponse

def home(request):
    return JsonResponse({"page": "home", "status": "ok"})
