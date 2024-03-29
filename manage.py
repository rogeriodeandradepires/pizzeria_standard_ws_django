#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import firebase_admin
from firebase_admin import db
from firebase_admin import credentials, firestore
from google.cloud import storage


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizzeria_standard_ws.settings')

    # cred = credentials.Certificate({
    #     "type": "service_account",
    #     "project_id": "dom-marino-ws",
    #     "private_key_id": "1128490a39d2566e37794e4b4e84a0121f352757",
    #     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDcVzvA89JZGrlK\nlsUtsVXTazTzmlKkvr524df7Ql1pBNIjpHsbh9GP8G4yv2S43meeNBAWm8yQNziJ\n2Al4Mpz46PUkbNO3IkOixfAXdtpEF5jZie5NRicSWFq+iha1IFB5TpHZ1TgrN5Kl\nGZCa6OyXv30enVrFgkqhqPV4lM+CU+9npE2zSz75XV7ljLxTbW86UCqzKnEyreLI\nxQK4zf2py3pjWor2vlb2HuaSklAW69QszkdldibodKS0ZiPh8HmZvPwuRnKcwUUT\nthkbCil+Y0AZhUf+XuQYNkJ40uj/z10fnKqGTPZ8tBYW60FM+1MPap5zViCX0voN\nCyt7A3mfAgMBAAECggEAS3myJTEf35fQ2qT0m+c/3/C8LamyH26bLXvFEPM1rhCR\nrtXbuZ13gle4V7fJ162PTtjEngn2M3xG6KjQ7ZRgwr6Bol2I1BVvl6U3zcHPmD2B\nBRtDPsMGBTmws833Y0nTZwor2bM4z0z09YrhRr78tCpKwJ7kBf3QdLm8g/ZtclWN\nNQCJC11zfyfff1NIMdoOzmzSH9vKPla6/3P83NIdQt97n5meb0tQ/amEyT5qLXvC\nRHA36zawrb5B27/pSvoxgZVxe4qT/hDs1BKbD9nZNW9jrtNPRrh1D2cEfsDcZcI5\nqd8hTelbfaQnJK+Fqqx9OyUId/GQ3dIPO/RRiEkLoQKBgQD3pIbI9zbt7OIN4PyK\nY9Om2dCtJAGKwnLlppKih2zyKHA2wHbKULQxRaEtSsFLbR/4Ern0MiqE55e5dOxj\nesiQMeSiH3qj53ZWzAyMoBNFRFw7N1LCTccwKARYM/x6nVUU0k/JH5EWAc3Zq//n\nktn4VQtQXrfItRJtqsZNm4/8sQKBgQDjxtX4u8b3phiCDRh/JftSY7fUWxpql/MV\nyT+oSe5tGQE9AoSIJ/DxJEoDvM3SBVtU5fKoTPsaBYccd0aycjko8BLLa+IbWyL2\nV6JCovsTciNJjcPWZJcoc2Gj9O2ona2d4pN9XkPNssUQuIZbIKK9tEqIMZVWK7mL\nwapaeTAvTwKBgFpzNGu4p851JAfPsk3VsluR2P80VH/bD95DXfGRJ0C3dmz5FSpG\nGdqZRQpm8HzdKb0REexYWmFauXcadrDLCvBn2MtCVigBhZ6kPr0qRn+ZPVq/lTG0\n+Njk9NlGe6RJTOci/dNG/VYdaJNlmD17zLNAVLaRMe1T/ZwisPVtqUSxAoGAEI3T\n4Tbsd/UnVNRU0nDVOiCrLJDOc67FaPDuYnG1FVK65082iJq2hSAJDQp8vuXKxHnN\nz/OAUFzUe/ojNjbc9p+0DfqyPSC7gsHNtiAYNUqXS/I0qHE5FySDlSHo39dN1eqw\no2zlap6yecufYCIYEcd3nzxTSSb2XjTeB6NFIDsCgYEAtJZM6GBS21djJjmjPEvM\n7s5VYzRi0AeKwf/Gpvdjd/MQcg1KEjlWww/g1YWDP+tVxt89XudMqO3sPDWjHJuZ\nSi8m3Kv1m4qqPE1RO/Fz5lFeM2fxL0xPz0dyF23pClrrVf+5wRbjfL4Zpd5MNuWr\nhmfG1frukywGXXTf+nwCjSc=\n-----END PRIVATE KEY-----\n",
    #     "client_email": "firebase-adminsdk-x049u@dom-marino-ws.iam.gserviceaccount.com",
    #     "client_id": "102254461450478082108",
    #     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    #     "token_uri": "https://oauth2.googleapis.com/token",
    #     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    #     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-x049u%40dom-marino-ws.iam.gserviceaccount.com"
    # })
    #
    # newDict = {'appName': 'Testando'}
    # firebase_admin.initialize_app(cred, newDict, 'Django')

    # client = storage.Client()

    # print('entrou')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
