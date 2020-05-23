import ast
from datetime import time

from django.core import serializers
from django.shortcuts import render

# Create your views here.
# pages/views.py
from django.http import HttpResponse, JsonResponse
from flask import Flask, jsonify, request, render_template
import os
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials, firestore
from google.cloud import storage
import json
import threading
from decimal import Decimal
import pysftp
import sys
import uuid
from standard_backend_app.apps import firebase_app

# cred = credentials.Certificate("dom-marino-ws-firebase-adminsdk-x049u-1128490a39.json")
# cred = credentials.Certificate({
#   "type": "service_account",
#   "project_id": "dom-marino-ws",
#   "private_key_id": "9bc70cb589de78815618d867a4194f2d35a3c447",
#   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCptuzwlf6G+RSQ\nRyQs5GUrFBDkYL++cvEGaGfi+gjdDdcTHF61BvesOvDnLDG+jaGrKz13a5TMKHwP\nik93IoNoIcXacmj3BMak5BpcjH3wvpktHAWooP6RkPn4qmCQ1dYE5zloqjWPbbcy\ngsmsGNf6NydcflFVhcqgjza7cTmT/eBzs9jgwE4cNThCULz8FHIlnlhHGVmy6dAm\nat1I4YMPe7X6EbJlJi13dwHBzRUWz4hO5zHv8hArQGskJtBTS/LZVuz+GmqFqmZN\n4AVX1METg4hjMUSevPIDyMgmRJt6R3sq3cV91AMCd75pmHeuVjIYYDqB7nqJWUrc\nBrgyOzUTAgMBAAECggEABkCpiRGVn4Zktg4Q7KB7g7NJDgjsd4lHjPtivG+GzRIZ\n9ufIK3Y2wL8pKfMsX/9a0fIVYSVzBXSGYZIwbEy2t6rq3anyaQthgCixOfCpISn8\nfbd3E+feiSFkvD8WsK9YI7UbHdqLf53ErpU39eGyb1MB3bv/ph14QiMUmqJIw0V7\nTrCn9QDVnHKiyll01tdBINaPp8vERO5BD6dGaXgiiS9oABOP+Y+As8DUEWNe3hHY\n6vw7Y4oQLrU5Roi/s4EwsdPSG4kq7P0gQTleoakXNHEBSJPfy1LbUlEuWCUeQEE0\npP+F7nGitzO3siRJ4RpIlIWCUYlxSVkX6phhIkw6bQKBgQDfYlPa9T0QixaRceA7\neHt3Q/kV/Fnz0qYyy7cRGxK8wjXK2nAD7+AVgJo2xnb6RyVJCMSgrY8nOCAJ2D4a\nS2I2MR3K0gmBhm4kmnGycEcTR9FTRy3Plg9fRXKRHfQ/l9qnuogOoHOHKq36UBKJ\nRmFD+nlHWAGstmdMtem8ONbKpwKBgQDCfohfSb0r78ZcET+OC+/st5YLfdxIfGKT\nPRXdYdyOtdIr2rU85CBfnF2vw1xwbv/dUteezUkfQmQUWOUHOFNRW1pGBi+AtCnV\n1dK+8SAP62AsJDa7/1TrhZzPrOxjKSYrk/EaX60EhxwABPSsXQTQjmLpTGipRGfr\nNAY3pelLtQKBgDL3s1xNAh7JLWAIFHpdNgZzStzaVAfOsz75vg44GCFbSny7ND2h\nuIYPbqA6ziCypO4yAvMKRpRTOPQmE51aP9FPiZWiMKsN6gmN940YEw9yHm+a2Pf5\nLA63wLkdlYIA+tG0PKDhuRpJAaMQK/qIRV8GQi+mA9PNVmppQyg/67oXAoGAVy3g\nctXatZcEksAofMNdB/5Cg2QnGVan2NfItTLoag+V5ZJjKqgW2sR8OgyXos4eYlZ/\nz+60mA5qTbSK9HGK5yzLihe7szUOi4sMrAnpFTmsIh0Za6tHpUp+v5gDXW9UbLQj\nnm7EXwMwydFu2tPXFKS+MVTOlRDUg9kN8GOt7wECgYBDKvUeY0p8vWaxYu73AGv4\n0deUc1NIhs/E9F5PnDlss23zekLjRKgy7KGgaU5XtuZvhinl5jr+xB4GdtEfLrj/\nfp+5HwBNsolOtLYkUCjxu0sW5fn9wyXNHIiFplSLVaLvhvbUyY7HS5D/0A2HxLjF\nc14i7d+midG1qptj3LVnfA==\n-----END PRIVATE KEY-----\n",
#   "client_email": "firebase-adminsdk-es2ca@dom-marino-ws.iam.gserviceaccount.com",
#   "client_id": "116197900106350835475",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-es2ca%40dom-marino-ws.iam.gserviceaccount.com"
# })
# #
# newDict = {'appName': 'Testando'}
# firebase_admin.initialize_app(cred, newDict, 'Django')
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dom-marino-ws-firebase-adminsdk-x049u-1128490a39.json"
# if not firebase_admin._apps:
#     firebase_admin.initialize_app(cred, newDict, 'Django')


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dom-marino-ws-firebase-adminsdk-x049u-1128490a39.json"

client = storage.Client()
# # https://console.cloud.google.com/storage/browser/[bucket-id]/
bucket = client.get_bucket('dom-marino-ws.appspot.com')
db = firestore.client()
# print(db.collection('todos').document('GetRkRdqhNTrdQ2wcvGE').get().to_dict())

imageurl = ''
thumbnailurl = ''

todo_ref = db.collection('todos')
categories_ref = db.collection('categories')
users_ref = db.collection('users')
orders_ref = db.collection('orders')
non_alcoholic_beverages_ref = db.collection('products').document('non_alcoholic_beverages').collection(
    'non_alcoholic_beverages')
alcoholic_beverages_ref = db.collection('products').document('alcoholic_beverages').collection('alcoholic_beverages')
beers_ref = db.collection('products').document('beers').collection('beers')
candy_pizzas_ref = db.collection('products').document('candy_pizzas').collection('candy_pizzas')
flapts_ref = db.collection('products').document('flapts').collection('flapts')
gourmet_pizzas_ref = db.collection('products').document('gourmet_pizzas').collection('gourmet_pizzas')
pizza_edges_ref = db.collection('products').document('pizza_edges').collection('pizza_edges')
traditional_pizzas_ref = db.collection('products').document('traditional_pizzas').collection('traditional_pizzas')
wines_ref = db.collection('products').document('wines').collection('wines')
promotions_ref = db.collection('products').document('promotions').collection('promotions')
two_flavored_pizzas_ref = db.collection('products').document('two_flavored_pizzas').collection('two_flavored_pizzas')
users_ref = db.collection('users')
working_hours_ref = db.collection('workinghours')

accounts = [
    {'name': "Billy", 'balance': 450.0},
    {'name': "Kelly", 'balance': 250.0}
]

all_categories = []
all_non_alcoholic_beverages = []
all_alcoholic_beverages = []
all_beers = []
all_pizza_edges = []
all_flapts = []
all_candy_pizzas = []
all_gourmet_pizzas = []
all_traditional_pizzas = []
all_wines = []
all_promotions = []
all_two_flavored_pizzas = []
all_orders = []
all_users = []

def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(u'Received document snapshot: {}'.format(doc.id))


def on_categories_snapshot(doc_snapshot, changes, read_time):
    # print("entrou")
    # print("on_categories_snapshot, closed=", cat_watch._closed)

    global all_categories
    all_categories = []

    for doc in doc_snapshot:
        category = doc.to_dict()
        all_categories.append(category)
        # print(category["description"])


def on_nab_snapshot(doc_snapshot, changes, read_time):
    global all_non_alcoholic_beverages
    all_non_alcoholic_beverages = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = non_alcoholic_beverages_ref.document(doc.id).collection('images').stream()
        prices = non_alcoholic_beverages_ref.document(doc.id).collection('prices').stream()
        price_broto_stream = non_alcoholic_beverages_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = non_alcoholic_beverages_ref.document(doc.id).collection('prices').document(
            'inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        size_prices = {'prices': {}}

        for size_id in prices:
            size_prices['prices'][size_id.id] = size_id.to_dict()

        product.update(size_prices)
        all_non_alcoholic_beverages.append(product)


def on_ab_snapshot(doc_snapshot, changes, read_time):
    global all_alcoholic_beverages
    all_alcoholic_beverages = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = alcoholic_beverages_ref.document(doc.id).collection('images').stream()
        prices = alcoholic_beverages_ref.document(doc.id).collection('prices').stream()
        price_broto_stream = alcoholic_beverages_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = alcoholic_beverages_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        size_prices = {'prices': {}}

        for size_id in prices:
            size_prices['prices'][size_id.id] = size_id.to_dict()

        product.update(size_prices)

        all_alcoholic_beverages.append(product)


def on_beers_snapshot(doc_snapshot, changes, read_time):
    global all_beers
    all_beers = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = beers_ref.document(doc.id).collection('images').stream()
        prices = beers_ref.document(doc.id).collection('prices').stream()
        price_broto_stream = beers_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = beers_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        size_prices = {'prices': {}}

        for size_id in prices:
            size_prices['prices'][size_id.id] = size_id.to_dict()

        product.update(size_prices)

        all_beers.append(product)


def on_candy_pizzas_snapshot(doc_snapshot, changes, read_time):
    global all_candy_pizzas
    all_candy_pizzas = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = candy_pizzas_ref.document(doc.id).collection('images').stream()
        prices = candy_pizzas_ref.document(doc.id).collection('prices').stream()
        price_broto_stream = candy_pizzas_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = candy_pizzas_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        size_prices = {'prices': {}}

        for size_id in prices:
            size_prices['prices'][size_id.id] = size_id.to_dict()

        product.update(size_prices)

        all_candy_pizzas.append(product)


def on_flapts_snapshot(doc_snapshot, changes, read_time):
    global all_flapts
    all_flapts = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = flapts_ref.document(doc.id).collection('images').stream()
        prices = flapts_ref.document(doc.id).collection('prices').stream()
        price_broto_stream = flapts_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = flapts_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        size_prices = {'prices': {}}

        for size_id in prices:
            size_prices['prices'][size_id.id] = size_id.to_dict()

        product.update(size_prices)

        all_flapts.append(product)


def on_pizza_edges_snapshot(doc_snapshot, changes, read_time):
    global all_pizza_edges
    all_pizza_edges = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = pizza_edges_ref.document(doc.id).collection('images').stream()
        prices = pizza_edges_ref.document(doc.id).collection('prices').stream()
        price_broto_stream = pizza_edges_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = pizza_edges_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        size_prices = {'prices': {}}

        for size_id in prices:
            size_prices['prices'][size_id.id] = size_id.to_dict()

        product.update(size_prices)

        all_pizza_edges.append(product)


def on_traditional_pizzas_snapshot(doc_snapshot, changes, read_time):
    global all_traditional_pizzas
    all_traditional_pizzas = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = traditional_pizzas_ref.document(doc.id).collection('images').stream()
        prices = traditional_pizzas_ref.document(doc.id).collection('prices').stream()
        price_broto_stream = traditional_pizzas_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = traditional_pizzas_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        size_prices = {'prices': {}}

        for size_id in prices:
            size_prices['prices'][size_id.id] = size_id.to_dict()

        product.update(size_prices)

        all_traditional_pizzas.append(product)
        # print(product)


def on_gourmet_pizzas_snapshot(doc_snapshot, changes, read_time):
    global all_gourmet_pizzas
    all_gourmet_pizzas = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = gourmet_pizzas_ref.document(doc.id).collection('images').stream()
        prices = gourmet_pizzas_ref.document(doc.id).collection('prices').stream()
        price_broto_stream = gourmet_pizzas_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = gourmet_pizzas_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        size_prices = {'prices': {}}

        for size_id in prices:
            size_prices['prices'][size_id.id] = size_id.to_dict()

        product.update(size_prices)

        all_gourmet_pizzas.append(product)


def on_wines_snapshot(doc_snapshot, changes, read_time):
    global all_wines
    all_wines = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = wines_ref.document(doc.id).collection('images').stream()
        prices = wines_ref.document(doc.id).collection('prices').stream()
        price_broto_stream = wines_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = wines_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        size_prices = {'prices': {}}

        for size_id in prices:
            size_prices['prices'][size_id.id] = size_id.to_dict()

        product.update(size_prices)

        all_wines.append(product)


def on_promotions_snapshot(doc_snapshot, changes, read_time):
    global all_promotions
    all_promotions = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = promotions_ref.document(doc.id).collection('images').stream()
        prices = promotions_ref.document(doc.id).collection('prices').stream()
        price_broto_stream = promotions_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = promotions_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        size_prices = {'prices': {}}

        for size_id in prices:
            size_prices['prices'][size_id.id] = size_id.to_dict()

        product.update(size_prices)

        all_promotions.append(product)


def on_two_flavored_pizzas_snapshot(doc_snapshot, changes, read_time):
    global all_two_flavored_pizzas
    all_two_flavored_pizzas = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = two_flavored_pizzas_ref.document(doc.id).collection('images').stream()
        prices = two_flavored_pizzas_ref.document(doc.id).collection('prices').stream()
        price_broto_stream = two_flavored_pizzas_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = two_flavored_pizzas_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        size_prices = {'prices': {}}

        for size_id in prices:
            size_prices['prices'][size_id.id] = size_id.to_dict()

        product.update(size_prices)

        all_two_flavored_pizzas.append(product)


def on_users_snapshot(doc_snapshot, changes, read_time):
    global all_users
    all_users = []

    for doc in doc_snapshot:
        user = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        all_users.append(user)


# Watch the document
cat_watch = categories_ref.on_snapshot(on_categories_snapshot)
nab_watch = non_alcoholic_beverages_ref.on_snapshot(on_nab_snapshot)
ab_watch = alcoholic_beverages_ref.on_snapshot(on_ab_snapshot)
beers_watch = beers_ref.on_snapshot(on_beers_snapshot)
candy_pizzas_watch = candy_pizzas_ref.on_snapshot(on_candy_pizzas_snapshot)
flapts_watch = flapts_ref.on_snapshot(on_flapts_snapshot)
pizza_edges_watch = pizza_edges_ref.on_snapshot(on_pizza_edges_snapshot)
traditional_pizzas_watch = traditional_pizzas_ref.on_snapshot(on_traditional_pizzas_snapshot)
gourmet_pizzas_watch = gourmet_pizzas_ref.on_snapshot(on_gourmet_pizzas_snapshot)
wines_watch = wines_ref.on_snapshot(on_wines_snapshot)
promotions_watch = promotions_ref.on_snapshot(on_promotions_snapshot)
two_flavored_pizzas_watch = two_flavored_pizzas_ref.on_snapshot(on_two_flavored_pizzas_snapshot)
users_watch = users_ref.on_snapshot(on_users_snapshot)

def monitor_watches():
    global cat_watch
    global nab_watch
    global ab_watch
    global beers_watch
    global candy_pizzas_watch
    global flapts_watch
    global pizza_edges_watch
    global traditional_pizzas_watch
    global gourmet_pizzas_watch
    global wines_watch
    global promotions_watch
    global two_flavored_pizzas_watch
    global users_watch

    threading.Timer(30.0, monitor_watches).start()

    if cat_watch._closed:
        cat_watch = categories_ref.on_snapshot(on_categories_snapshot)

    if nab_watch._closed:
        nab_watch = non_alcoholic_beverages_ref.on_snapshot(on_nab_snapshot)

    if ab_watch._closed:
        ab_watch = alcoholic_beverages_ref.on_snapshot(on_ab_snapshot)

    if beers_watch._closed:
        beers_watch = beers_ref.on_snapshot(on_beers_snapshot)

    if candy_pizzas_watch._closed:
        candy_pizzas_watch = candy_pizzas_ref.on_snapshot(on_candy_pizzas_snapshot)

    if flapts_watch._closed:
        flapts_watch = flapts_ref.on_snapshot(on_flapts_snapshot)

    if pizza_edges_watch._closed:
        pizza_edges_watch = pizza_edges_ref.on_snapshot(on_pizza_edges_snapshot)

    if traditional_pizzas_watch._closed:
        traditional_pizzas_watch = traditional_pizzas_ref.on_snapshot(on_traditional_pizzas_snapshot)

    if gourmet_pizzas_watch._closed:
        gourmet_pizzas_watch = gourmet_pizzas_ref.on_snapshot(on_gourmet_pizzas_snapshot)

    if wines_watch._closed:
        wines_watch = wines_ref.on_snapshot(on_wines_snapshot)

    if promotions_watch._closed:
        promotions_watch = promotions_ref.on_snapshot(on_promotions_snapshot)

    if two_flavored_pizzas_watch._closed:
        two_flavored_pizzas_watch = two_flavored_pizzas_ref.on_snapshot(on_two_flavored_pizzas_snapshot)

    if users_watch._closed:
        users_watch = users_ref.on_snapshot(on_users_snapshot)


monitor_watches()

def setImageUrl(url):
    global imageurl
    imageurl = url

def homePageView(request):
    return HttpResponse('Hello, World!')

def list_categories(request):
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """

    while len(all_categories) == 0:
        time.sleep(1)

    try:
        # Check if ID was passed to URL query
        cat_id = request.GET.get('id')
        if cat_id:
            category = object
            for element in all_categories:
                if element['id'] == cat_id:
                    category = element
            # data = json.dumps(category)
            data = dict(category)
            # serializers.serialize('json', [category, ])
            # nab = non_alcoholic_beverages_ref.document(nab_id).get()
            print("return object: ", data)
            return JsonResponse(data, content_type="application/json")
        else:
            # all_nab = [doc.to_dict() for doc in non_alcoholic_beverages_ref.stream()]
            # return jsonify(all_categories), 200

            # data = json.dumps(all_categories)
            # data = jsonify(all_categories)
            # data = {'': all_categories}

            # for category in all_categories:
            #     data.copy(dict(category))
            #     # data.append(dict(category))

            # print("return list: ", all_categories)

            # data = json.loads()
            return JsonResponse(all_categories, safe=False, content_type="application/json")
            # return JsonResponse(response, safe=False)
    except Exception as e:
        return f"An Error Occured: {e}"

# @app.route('/get_working_hours', methods=['GET'])
def get_working_hours(request):
    # week_day = request.args.get('weekDay')
    week_day = request.GET.get('weekDay')
    # print(week_day)
    docSnapshot = working_hours_ref.document(week_day).get()

    # data = json.dumps(jsonify(docSnapshot.to_dict()))
    data = docSnapshot.to_dict()
    # print(docSnapshot.to_dict())

    # return jsonify(docSnapshot.to_dict()), 200
    return JsonResponse(data, content_type="application/json")
    # return HttpResponse(docSnapshot.to_dict())