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

# add new Order
def addOrder(name, room):
    from drjava.models import Order

    newOrder = Order(name=name, room=room)
    newOrder.save()

    print("Added new order: ")
    print(str(newOrder))

    print("Added face:")
    print(newFace)


# -----------------------------------------------------------------------

# Get all the orders
def getOrders():
    from drjava.models import Order

    allOrders = Order.objects.all()

    orders_list = []
    for order in allOrders:
        order_dict = {"name": order.name, "room": order.room}
        orders_list.append(order_dict)

    return orders_list


# -----------------------------------------------------------------------

# Get all the orders
def deleteOrder(name, room):
    from drjava.models import Order

    matchingOrders = Order.objects.filter(name=name, room=room)

    for order in matchingOrders:
        print("Deleting: " + str(order))
        order.delete()


# -----------------------------------------------------------------------


def main():

    pass


# -----------------------------------------------------------------------

if __name__ == "__main__":
    main()
