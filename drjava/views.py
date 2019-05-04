from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
import json
from . import access

# Create your views here.
def index(request):
    return render(request, "drjava/index.html", {})


def ordered(request):
    return render(request, "drjava/ordered.html", {})

def interact(request):
    currentFace = request.GET.get("currentFace", "Brian Kernighan")
    access.addFace(currentFace)

    ret_val = {"currentFace": currentFace}
    return JsonResponse(ret_val, safe=False)

def getface(request):
    currentFace = access.getFace()
    
    ret_val = {"currentFace": currentFace}
    return JsonResponse(ret_val, safe=False)