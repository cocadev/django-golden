from datetime import datetime
import random


class InvoiceState():
    states = {
        "received": 1,
        "in-progress": 2,
        "delivered": 3,
        "canceled": 4,
        "returned": 5,
    }

    RECEIVED = 0
    IN_PROGRESS = 1
    PENDING = 2
    DELIVERED = 3
    CANCELED = 4
    RETURNED = 5
    ERROR = 6


def createInvoice(clientID):
    return "INV-" + datetime.now().strftime("%Y%m%d%H%M%S") + random.choice(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ') + str(clientID)


class Units():
    choices = (
        ('Mass', (
            ('kg', 'Kilogram'),
            ('g', 'Gram'),
        )
         ),
        ('Length', (
            ('mm', 'Millimeter'),
            ('m', 'Meter'),
        )
         ),
        ('box', 'Box'),
        ('pallet', 'Pallet'),
        ('unit', 'Unit'),
        ('l', 'Litter'),
    )