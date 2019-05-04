from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
import json

# Create your views here.
def index(request):
    return render(request, "drjava/index.html", {})


def ordered(request):
    return render(request, "drjava/ordered.html", {})

def interact(request):
    currentFace = request.GET.get("currentFace", "Brian Kernighan")

    ret_val = {"currentFace": currentFace}
    return JsonResponse(ret_val, safe=False)