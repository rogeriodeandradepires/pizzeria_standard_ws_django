import firebase_admin
from django.apps import AppConfig
from firebase_admin import firestore

firebase_app = None


class PizzariaStandardWsProjectConfig(AppConfig):
    name = 'standard_backend_app'

    def ready(self):
        cred = 

        cred2 = 

        global firebase_app
        firebase_app = firebase_admin.initialize_app(cred2)
