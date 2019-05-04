#!/usr/bin/env python

import os
import sys
import django
import datetime
from datetime import date
import json

# path = "/Users/marora/repos/notifymeal"
# if path not in sys.path:
#     sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

# -----------------------------------------------------------------------

# add a Face
def addFace(face):
    from drjava.models import Face

    delFaces()
    newFace = Face(name=face, creation=datetime.datetime.now())
    newFace.save()

    print("Added face:")
    print(newFace)

# -----------------------------------------------------------------------

# delete all faces
def delFaces():
    from drjava.models import Face
    try:
        Face.objects.all().delete()
    except: 
        print("No faces to delete")

# -----------------------------------------------------------------------

# Get face in the last minute
def getFace():
    from drjava.models import Face

    d = datetime.timedelta(seconds=120)
    start = datetime.datetime.now() - d 

    thisFace = Face.objects.filter(creation__gte=start)
    if thisFace.count() == 0:
        print("No Face found")
        return "NO DATA"
    else:
        thisFace = thisFace.last()
    
    return thisFace.name

# -----------------------------------------------------------------------

def main():

    pass


# -----------------------------------------------------------------------

if __name__ == "__main__":
    main()
