from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "drjava/index.html", {})


def ordered(request):
    return render(request, "drjava/ordered.html", {})

