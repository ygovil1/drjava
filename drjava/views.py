from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
import json
from . import access
from . import verifyName

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

    ret_val = verifyName.findInfo(currentFace)
    return JsonResponse(ret_val, safe=False)


def getInstruction(request):
    x = request.GET.get("xpos", "225")
    x = int(x)

    y = request.GET.get("ypos", "77")
    y = int(y)

    move_magnitude = 3.0
    move_direction = "x"
    if x > 225:
        move_direction = "-x"

    arm_req = False

    if x < 75 and y < 98:
        arm_req = True

    floor_to = 3

    instruction = {
        "move_magnitude": move_magnitude,
        "move_direction": move_direction,
        "arm_req": arm_req,
        "floor_to": floor_to,
    }

    return JsonResponse(instruction, safe=False)
