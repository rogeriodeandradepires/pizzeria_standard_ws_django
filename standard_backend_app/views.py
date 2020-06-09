import ast
from datetime import time

import MySQLdb
from django.db import connections

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
import MySQLdb.cursors
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
from standard_backend_app.models import Categoria

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dom-marino-ws-firebase-adminsdk-x049u-1128490a39.json"

client = storage.Client()
# # https://console.cloud.google.com/storage/browser/[bucket-id]/
bucket = client.get_bucket('dom-marino-ws.appspot.com')
db = firestore.client()
# print(db.collection('todos').document('GetRkRdqhNTrdQ2wcvGE').get().to_dict())



# cursor = connections['adminNeto'].cursor() # Replace 'cust' to other defined databases if necessary.
# cursor.execute("select * from ockf_product")
# results = cursor.fetchall()
# cursor.close()

# conn = MySQLdb.connect(host='144.217.28.12',
#                          user='kingticom_oca639',
#                          passwd='tst.2020.app',
#                          port=3303,
#                          db='kingticom_oca639',)
# cursor = conn.cursor(MySQLdb.cursors.DictCursor)
# cursor.execute("select * from ockf_product")
# results = cursor.fetchall()
# cursor.close()
# print(results)

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

    querySetTuple = Categoria.objects.values()
    all_categories_db = [entry for entry in querySetTuple]

    for doc in doc_snapshot:
        category = doc.to_dict()
        all_categories.append(category)

        if category not in all_categories_db:
            m = Categoria(**category)
            m.save(using='standard')
        # else:
        #     print('já tem na lista: ', category)


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


#Watch the document
# cat_watch = categories_ref.on_snapshot(on_categories_snapshot)
# nab_watch = non_alcoholic_beverages_ref.on_snapshot(on_nab_snapshot)
# ab_watch = alcoholic_beverages_ref.on_snapshot(on_ab_snapshot)
# beers_watch = beers_ref.on_snapshot(on_beers_snapshot)
# candy_pizzas_watch = candy_pizzas_ref.on_snapshot(on_candy_pizzas_snapshot)
# flapts_watch = flapts_ref.on_snapshot(on_flapts_snapshot)
# pizza_edges_watch = pizza_edges_ref.on_snapshot(on_pizza_edges_snapshot)
# traditional_pizzas_watch = traditional_pizzas_ref.on_snapshot(on_traditional_pizzas_snapshot)
# gourmet_pizzas_watch = gourmet_pizzas_ref.on_snapshot(on_gourmet_pizzas_snapshot)
# wines_watch = wines_ref.on_snapshot(on_wines_snapshot)
# promotions_watch = promotions_ref.on_snapshot(on_promotions_snapshot)
# two_flavored_pizzas_watch = two_flavored_pizzas_ref.on_snapshot(on_two_flavored_pizzas_snapshot)
# users_watch = users_ref.on_snapshot(on_users_snapshot)

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


# monitor_watches()

def setImageUrl(url):
    global imageurl
    imageurl = url

# def homePageView(request):
#     return HttpResponse('Hello, World!')

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

def create_user(request):
    # user_id = users_ref.document().id

    # print("Posted file: {}".format(request.files['image_file']))
    # file = request.files['image_file']
    # files = {'file': file.read()}

    print(request)

    uid = request.POST['uid']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    street = request.POST['street']
    streetNumber = request.POST['streetNumber']
    neighborhood = request.POST['neighborhood']
    city = request.POST['city']
    imgUrl = request.POST['img_url']
    isRegisterComplete = request.POST['isRegisterComplete']

    # print('entrou2', file=sys.stdout, flush=True)

    if request.POST['hasImageFile'] == "True":
        image = request.FILES['image_file'].read()
        print('imagem não é nula', file=sys.stdout, flush=True)
        # print(u'Received document snapshot: {}'.format(doc.id))

        # session = ftplib.FTP_TLS('157.230.167.73', 'root', '27031984As')
        # # file = open('kitten.jpg', 'rb')  # file to send
        # session.storbinary('STOR /var/www/powermemes.com/dommarino/{}.jpg'.format(uid), image)  # send the file
        # image.close()  # close file and FTP
        # session.quit()

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        with pysftp.Connection(host='157.230.167.73', username='root', password='27031984As', cnopts=cnopts) as sftp:
            print("Connection succesfully stablished ... ")

            # Switch to a remote directory

            if not sftp.isdir('/var/www/powermemes.com/htdocs/pizzerias/dommarino/userimg/{}'.format(uid)):
                sftp.mkdir('/var/www/powermemes.com/htdocs/pizzerias/dommarino/userimg/{}'.format(uid))


            sftp.cwd('/var/www/powermemes.com/htdocs/pizzerias/dommarino/userimg/{}'.format(uid))

            img_id = str(uuid.uuid1())

            print('imge id={}'.format(img_id))

            f = sftp.open('/var/www/powermemes.com/htdocs/pizzerias/dommarino/userimg/{0}/{1}.png'.format(uid, img_id), 'wb')
            f.write(image)

            # sftp.put(image.file.name, '/var/www/powermemes.com/dommarino/{}.jpg'.format(uid))

        # print(products_id)
        imgUrl = "https://powermemes.com/pizzerias/dommarino/userimg/{0}/{1}.png".format(uid, img_id)

    elif imgUrl=="":
        imgUrl="https://powermemes.com/pizzerias/dommarino/userimg/avatar.png"

    data = {
        u'uid': u'{}'.format(uid),
        u'name': u'{}'.format(name),
        u'email': u'{}'.format(email),
        u'phone': u'{}'.format(phone),
        u'street': u'{}'.format(street),
        u'streetNumber': u'{}'.format(streetNumber),
        u'neighborhood': u'{}'.format(neighborhood),
        u'city': u'{}'.format(city),
        u'image_url': u'{}'.format(imgUrl),
        u'isRegisterComplete': u'{}'.format(isRegisterComplete),
    }

    users_ref.document(uid).set(data)

    print(data)
    return JsonResponse({"success": True}, content_type="application/json")
    # jsonify({"success": True}), 200
    # print(image)

def makeorder(request):

    # dd/mm/YY
    # today = datetime.now()
    # # today = today.strftime("%d-%m-%Y")
    # today = today.strftime("%Y-%m-%d %H:%M:%S")

    request_json = json.loads(request.body)

    # print(json.loads(request.body)['date_time'])
    today = request_json['date_time']#.get('date_time')
    # print('entrou')


    startdata = {
        u'id': u'{0}'.format(today[:-9])
    }

    thisOrderRef = orders_ref.document(today[:-9])

    thisOrderRef.set(startdata)
    thisOrderRef = thisOrderRef.collection(today[:-9])
    order_ref_for_update = thisOrderRef

    # print("hoje é: {0}".format(today))

    try:
        coupon_id = request_json['coupon_id']
        delivery = request_json['delivery']
        payment_method = request_json['payment_method']
        payment_change = request_json['payment_change']
        delivery_address = request_json['delivery_address']
        total = request_json['total']
        userId = request_json['userId']
        id = thisOrderRef.document().id
        products_id = request_json['products_id']

        # print(products_id)

        data = {
            u'coupon_id': u'{}'.format(coupon_id),
            u'dateTime': u'{}'.format(today),
            u'id': u'{}'.format(id),
            u'delivery': u'{}'.format(delivery),
            u'payment_method': u'{}'.format(payment_method),
            u'payment_change': u'{}'.format(payment_change),
            u'delivery_address': u'{}'.format(delivery_address),
            u'total': u'{}'.format(total),
            u'userId': u'{}'.format(userId)
        }

        thisOrderRef.document(id).set(data)
        thisOrderRef = thisOrderRef.document(id).collection('products_id')

        #product.update({'price_broto': None})
        # product_dict = literal_eval(products_id)
        json_acceptable_string = products_id.replace("'", "\"")
        product_dict = json.loads(json_acceptable_string)
        # print(product_dict)

        total_paid = Decimal('0.00')

        for key, value in product_dict.items():
            product = value
            thisId = thisOrderRef.document().id

            paid_price = 0.00
            pizza_edge_price = 0.00
            pizza_edge_description = ""
            product_description = ""
            img_url = ""
            all_items = []

            if product.get("isTwoFlavoredPizza") == 0:
                if product.get("product1_category") == "beers":
                    all_items.extend(all_beers)
                elif product.get("product1_category") == "alcoholic_beverages":
                    all_items.extend(all_alcoholic_beverages)
                elif product.get("product1_category") == "flapts":
                    all_items.extend(all_flapts)
                elif product.get("product1_category") == "non_alcoholic_beverages":
                    all_items.extend(all_non_alcoholic_beverages)
                elif product.get("product1_category") == "promotions":
                    all_items.extend(all_promotions)
                elif product.get("product1_category") == "wines":
                    all_items.extend(all_wines)
                elif product.get("product1_category") == "candy_pizzas":
                    all_items.extend(all_candy_pizzas)
                elif product.get("product1_category") == "gourmet_pizzas":
                    all_items.extend(all_gourmet_pizzas)
                elif product.get("product1_category") == "traditional_pizzas":
                    all_items.extend(all_traditional_pizzas)

                if "pizza" not in product.get("product1_category"):
                    for item in all_items:
                        if item.get('id') == product.get("product_id"):
                            paid_price = item.get("price")
                            product_description = item.get('description')
                            img_url = item.get('image')

                else:
                    if product.get("pizza_edge_id") != "null":
                        for pizza_edge in all_pizza_edges:
                            if pizza_edge.get('id') == product.get("pizza_edge_id"):
                                pizza_edge_description = pizza_edge.get("description")
                                if product.get("size") == "Broto":
                                    pizza_edge_price = pizza_edge.get("price_broto")
                                if product.get("size") == "Inteira":
                                    pizza_edge_price = pizza_edge.get("price_inteira")

                    for item in all_items:
                        if item.get('id') == product.get("product_id"):
                            product_description = item.get('description')
                            img_url = item.get('image')

                            if product.get("size") == "Broto":
                                paid_price = item.get("price_broto")
                            if product.get("size") == "Inteira":
                                paid_price = item.get("price_inteira")

                    new_price = Decimal(paid_price)+Decimal(pizza_edge_price)
                    paid_price = round(new_price, 2)
            else:
                product1_price = 0.00
                product2_price = 0.00

                if product.get("pizza_edge_id") != "null":
                    for pizza_edge in all_pizza_edges:
                        if pizza_edge.get('id') == product.get("pizza_edge_id"):
                            pizza_edge_description = pizza_edge.get("description")
                            if product.get("size") == "Broto":
                                pizza_edge_price = pizza_edge.get("price_broto")
                            if product.get("size") == "Inteira":
                                pizza_edge_price = pizza_edge.get("price_inteira")

                if product.get("product1_category") == "traditional_pizzas":
                    all_items.extend(all_traditional_pizzas)
                elif product.get("product1_category") == "gourmet_pizzas":
                    all_items.extend(all_gourmet_pizzas)
                elif product.get("product1_category") == "candy_pizzas":
                    all_items.extend(all_candy_pizzas)

                for product1 in all_items:
                    if product1.get('id') == product.get("product_id"):
                        product_description = product1.get('description')
                        img_url = "https://storage.googleapis.com/dom-marino-ws.appspot.com/categories/custom/two_flavored_pizza_image.png"

                        if product.get("size") == "Broto":
                            product1_price = product1.get("price_broto")
                        if product.get("size") == "Inteira":
                            product1_price = product1.get("price_inteira")

                all_items = []
                if product.get("product2_category") == "traditional_pizzas":
                    all_items.extend(all_traditional_pizzas)
                elif product.get("product2_category") == "gourmet_pizzas":
                    all_items.extend(all_gourmet_pizzas)
                elif product.get("product2_category") == "candy_pizzas":
                    all_items.extend(all_candy_pizzas)

                for product2 in all_items:
                    if product2.get('id') == product.get("product2_id"):
                        product_description += " + "+product2.get('description')
                        if product.get("size") == "Broto":
                            product2_price = product2.get("price_broto")
                        if product.get("size") == "Inteira":
                            product2_price = product2.get("price_inteira")

                product1_decimal_price = Decimal(product1_price)
                product2_decimal_price = Decimal(product2_price)

                max_price = max(product1_decimal_price, product2_decimal_price)

                pizza_edge_decimal_price = Decimal(pizza_edge_price)
                max_price_decimal = Decimal(max_price)

                new_price = max_price_decimal+pizza_edge_decimal_price
                paid_price = new_price

            thisProduct = {
                u'category': u'{}'.format(product.get("category")),
                u'notes': u'{}'.format(product.get("notes")),
                u'id': u'{}'.format(thisId),
                u'paid_price': u'{}'.format(paid_price),
                u'pizza_edge_id': u'{}'.format(product.get("pizza_edge_id")),
                u'pizza_edge_description': u'{}'.format(pizza_edge_description),
                u'pizza_edge_paid_price': u'{}'.format(pizza_edge_price),
                u'product1_category': u'{}'.format(product.get("product1_category")),
                u'product2_category': u'{}'.format(product.get("product2_category")),
                u'product2_id': u'{}'.format(product.get("product2_id")),
                u'product_description': u'{}'.format(product_description),
                u'product_id': u'{}'.format(product.get("product_id")),
                u'product_image_url': u'{}'.format(img_url),
                u'quantity': u'{}'.format(product.get("quantity")),
                u'isTwoFlavoredPizza': u'{}'.format(product.get("isTwoFlavoredPizza")),
                u'size': u'{}'.format(product.get("size"))
            }

            total_paid += Decimal(paid_price)*Decimal(product.get("quantity"))

            thisOrderRef.document(thisId).set(thisProduct)

        delivery_tax_ref_snapshot = db.collection('delivery_tax').document('current_tax').get()
        tax = delivery_tax_ref_snapshot.to_dict()['value']

        if delivery_address.lower() != "retirada":
            total_paid += Decimal(tax)

        order_ref_for_update.document(id).update({u'total': str(round(total_paid, 2))})

        # print('chegou aqui')
        # return jsonify({"success": True}), 200
        return JsonResponse({"success": True}, content_type="application/json")
    except Exception as e:
        return f"An Error Occured: {e}"

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

def list_user_orders(request):
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    all_orders=[]
    user_id = request.GET.get('id')
    docSnapshot = orders_ref.stream()

    for doc in docSnapshot:
        data_stream = orders_ref.document(doc.id).collection(doc.id).where(u'userId', u'==', user_id).stream()

        for order in data_stream:
            thisOrder = order.to_dict()
            tempMap = dict()
            products_stream = orders_ref.document(doc.id).collection(doc.id).document(order.id).collection("products_id").stream()
            # thisProductDict = {}
            for product in products_stream:
                thisProduct = product.to_dict()
                # thisOrder["products_id"][product.id] = thisProduct
                tempMap[product.id] = thisProduct


            thisOrder.update({"products_id": tempMap})
            # print(thisProduct)

            all_orders.append(thisOrder)


    try:
        # Check if ID was passed to URL query
        return JsonResponse(all_orders, safe=False, content_type="application/json")
    except Exception as e:
        return f"An Error Occured: {e}"

def list_users(request):
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """

    try:
        # Check if ID was passed to URL query
        user_id = request.GET.get('uid')

        if user_id:
            user_snapshot = users_ref.document(user_id).get()
            user = user_snapshot.to_dict()
            return JsonResponse(user, content_type="application/json")
        else:
            # all_nab = [doc.to_dict() for doc in non_alcoholic_beverages_ref.stream()]
            return JsonResponse(all_users, safe=False, content_type="application/json")
    except Exception as e:
        return f"An Error Occured: {e}"

def list_products(request):
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    # while len(all_traditional_pizzas) == 0:
    #     time.sleep(1)

    # print(request.GET)

    try:
        # Check if ID was passed to URL query
        product_id = request.GET.get('id')
        category = request.GET.get('category')

        all_items = []
        if category == "beers":
            while len(all_beers) == 0:
                time.sleep(1)
            all_items.extend(all_beers)
        elif category == "alcoholic_beverages":
            while len(all_alcoholic_beverages) == 0:
                time.sleep(1)
            all_items.extend(all_alcoholic_beverages)
        elif category == "flapts":
            while len(all_flapts) == 0:
                time.sleep(1)
            all_items.extend(all_flapts)
        elif category == "non_alcoholic_beverages":
            while len(all_non_alcoholic_beverages) == 0:
                time.sleep(1)
            all_items.extend(all_non_alcoholic_beverages)
        elif category == "promotions":
            while len(all_promotions) == 0:
                time.sleep(1)
            all_items.extend(all_promotions)
        elif category == "wines":
            while len(all_wines) == 0:
                time.sleep(1)
            all_items.extend(all_wines)
        elif category == "candy_pizzas":
            while len(all_candy_pizzas) == 0:
                time.sleep(1)
            all_items.extend(all_candy_pizzas)
        elif category == "gourmet_pizzas":
            while len(all_gourmet_pizzas) == 0:
                time.sleep(1)
            all_items.extend(all_gourmet_pizzas)
        elif category == "traditional_pizzas":
            while len(all_traditional_pizzas) == 0:
                time.sleep(1)
            all_items.extend(all_traditional_pizzas)
        elif category == "pizza_edges":
            while len(all_pizza_edges) == 0:
                time.sleep(1)
            all_items.extend(all_pizza_edges)
        elif category == "two_flavored_pizzas":
            while len(all_two_flavored_pizzas) == 0:
                time.sleep(1)
            all_items.extend(all_two_flavored_pizzas)

        if product_id:
            product = object
            for element in all_items:
                if element['id'] == product_id:
                    product = element
            # nab = non_alcoholic_beverages_ref.document(nab_id).get()
            return JsonResponse(product, content_type="application/json")
        else:
            # all_nab = [doc.to_dict() for doc in non_alcoholic_beverages_ref.stream()]
            return JsonResponse(all_items, safe=False, content_type="application/json")


    except Exception as e:
        return f"An Error Occured: {e}"
