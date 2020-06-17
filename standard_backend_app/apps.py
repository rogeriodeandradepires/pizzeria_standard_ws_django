import firebase_admin
from django.apps import AppConfig
from firebase_admin import firestore

firebase_app = None


class PizzariaStandardWsProjectConfig(AppConfig):
    name = 'standard_backend_app'

    def ready(self):
        cred = firebase_admin.credentials.Certificate({
            "type": "service_account",
            "project_id": "dom-marino-ws",
            "private_key_id": "1128490a39d2566e37794e4b4e84a0121f352757",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDcVzvA89JZGrlK\nlsUtsVXTazTzmlKkvr524df7Ql1pBNIjpHsbh9GP8G4yv2S43meeNBAWm8yQNziJ\n2Al4Mpz46PUkbNO3IkOixfAXdtpEF5jZie5NRicSWFq+iha1IFB5TpHZ1TgrN5Kl\nGZCa6OyXv30enVrFgkqhqPV4lM+CU+9npE2zSz75XV7ljLxTbW86UCqzKnEyreLI\nxQK4zf2py3pjWor2vlb2HuaSklAW69QszkdldibodKS0ZiPh8HmZvPwuRnKcwUUT\nthkbCil+Y0AZhUf+XuQYNkJ40uj/z10fnKqGTPZ8tBYW60FM+1MPap5zViCX0voN\nCyt7A3mfAgMBAAECggEAS3myJTEf35fQ2qT0m+c/3/C8LamyH26bLXvFEPM1rhCR\nrtXbuZ13gle4V7fJ162PTtjEngn2M3xG6KjQ7ZRgwr6Bol2I1BVvl6U3zcHPmD2B\nBRtDPsMGBTmws833Y0nTZwor2bM4z0z09YrhRr78tCpKwJ7kBf3QdLm8g/ZtclWN\nNQCJC11zfyfff1NIMdoOzmzSH9vKPla6/3P83NIdQt97n5meb0tQ/amEyT5qLXvC\nRHA36zawrb5B27/pSvoxgZVxe4qT/hDs1BKbD9nZNW9jrtNPRrh1D2cEfsDcZcI5\nqd8hTelbfaQnJK+Fqqx9OyUId/GQ3dIPO/RRiEkLoQKBgQD3pIbI9zbt7OIN4PyK\nY9Om2dCtJAGKwnLlppKih2zyKHA2wHbKULQxRaEtSsFLbR/4Ern0MiqE55e5dOxj\nesiQMeSiH3qj53ZWzAyMoBNFRFw7N1LCTccwKARYM/x6nVUU0k/JH5EWAc3Zq//n\nktn4VQtQXrfItRJtqsZNm4/8sQKBgQDjxtX4u8b3phiCDRh/JftSY7fUWxpql/MV\nyT+oSe5tGQE9AoSIJ/DxJEoDvM3SBVtU5fKoTPsaBYccd0aycjko8BLLa+IbWyL2\nV6JCovsTciNJjcPWZJcoc2Gj9O2ona2d4pN9XkPNssUQuIZbIKK9tEqIMZVWK7mL\nwapaeTAvTwKBgFpzNGu4p851JAfPsk3VsluR2P80VH/bD95DXfGRJ0C3dmz5FSpG\nGdqZRQpm8HzdKb0REexYWmFauXcadrDLCvBn2MtCVigBhZ6kPr0qRn+ZPVq/lTG0\n+Njk9NlGe6RJTOci/dNG/VYdaJNlmD17zLNAVLaRMe1T/ZwisPVtqUSxAoGAEI3T\n4Tbsd/UnVNRU0nDVOiCrLJDOc67FaPDuYnG1FVK65082iJq2hSAJDQp8vuXKxHnN\nz/OAUFzUe/ojNjbc9p+0DfqyPSC7gsHNtiAYNUqXS/I0qHE5FySDlSHo39dN1eqw\no2zlap6yecufYCIYEcd3nzxTSSb2XjTeB6NFIDsCgYEAtJZM6GBS21djJjmjPEvM\n7s5VYzRi0AeKwf/Gpvdjd/MQcg1KEjlWww/g1YWDP+tVxt89XudMqO3sPDWjHJuZ\nSi8m3Kv1m4qqPE1RO/Fz5lFeM2fxL0xPz0dyF23pClrrVf+5wRbjfL4Zpd5MNuWr\nhmfG1frukywGXXTf+nwCjSc=\n-----END PRIVATE KEY-----\n",
            "client_email": "firebase-adminsdk-x049u@dom-marino-ws.iam.gserviceaccount.com",
            "client_id": "102254461450478082108",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-x049u%40dom-marino-ws.iam.gserviceaccount.com"
        })

        cred2 = firebase_admin.credentials.Certificate({
            "type": "service_account",
            "project_id": "standard-pizzeria",
            "private_key_id": "c8dadbf83fa6f4b4d830abaa07d37b767ecdf514",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDBDCn74dsdBWcs\n28MiMGpIuDkWQ74pQnT5dHj3lC3w70BS10A6hN5IP1MHZ7sLcqyZfveoQqPh2Tgr\nXvjKjeZsQdhzgqgyz/pyUKeAHiZF+8hM4CAuq1LDpYZICiS6MsDUqgtazaslf+kC\nlnffnc6L/TxZRnJJOGbVrJjluAVT/sSNr2KQdlhSbc14ZODTlRr+1SkSGLIubKvN\nduXQyGQPbyQ0XLkB6zhD4bzNVntUrdDZKXyyCM9Z2/s8dko8oY4SKN/4XkqG5yxl\n2O35EsdJFurdmbjNji1Fw3AAmcIPlVAFEMsr01TUkCcAGJJkDH003ffQbJ3npmMi\nZr20qT5bAgMBAAECggEAVzPLc0Be3gkmxhivWK5OFHNDNk97gt/GPzjhu9RvvDoW\n8FTTapvCXRhdxSaSU2WFmgDElnkj1k1tFgpckALxZ02HHQaUO/++vgy43SLBXzOR\nE0jawLobNM18juYmGQX8HRSC9I2bFeFlvAmENLrwJkRKEnnD/lc//J1uo7YwkfPl\n8/C0xu6iS3sIJo4cYo5wPu11+Y5jM5jbVsb8sgYILO03CC1HdYCMTLagIpqcNvh9\nPn3EdtWQf+dOz9+f2siG1FQa4vIF2AWEwYlKRnpukABQ7I6KDKSqSkHFDH2jOpx1\nts0P3Q0w1YaLSqolDuW18eRTNc1m/s9HMYtCNA8KIQKBgQDyf1anVUfUZueYxINa\nK4g9/qj1wq8Zcl6cbTp5NSwyVT8KmHfbBlaBco/mmg/uIabQ0+R0/Z9Z99TlPkXp\nGWJhZBmGBbhV9jIfiZKD/fo0ZV0iCerZt+7u/1YX+ZrW+MYnONj6Iw/fQspRYPiH\nPuF/ww1Ir386yDd1rWLj2UikhwKBgQDLy/IP8ezjO0bxsDHjNpsA7YORF4vwF3Dk\nha1C2V04uTUU0tHzF9c/4vhGrRPaWxON6tEg2K3iFhq+fM02ZfepyMXJDxLEtbB6\nRstYPPvSEHXOqj++/flBZcPb9+Qux4gkuPZHuoMSNCSsRrNu/014COJidX6N38So\nnbTH12xgjQKBgQDXm7zSHxM0mSJGREN9wsLqTCiyCp1hBL12W+/noQ1g20aoBxRa\nG3KCufeUU1rioe0OM7gnBPHQLniOMyY5sSY17ah7704MsE+0lr88uG7kc1OxVhwH\n5HB+82v6+SVhCeQ1L2hMTyxnl50Hai7PIWuiCy0eeVuoSih1aupIKANctQKBgQDL\nsnirKVNuOFSLxGHIyk6Z2cz0XAW6H6PuNhLcy2gbBzugKaxB/yVdrN4dvmcmjHv6\nEKeg3hLG9PMcTJ/M7JRkNtJCSXen+DaBsXsUIjhNWbh2rcJzg2T80du3ZInFnBhf\nJCS9wxW5PzccnrpAipwDC1ZDtU6ePfhR1PfZ+19PDQKBgBqmvfVscXTIZ1n53eti\ngbNq6H9Y9Irr1tfNqWHrmr6lKS/AuzcH4fWuHIlDqtQyAuxVtWWK683Dd36/Noad\nZ4RO5yTQYK5PNGG5KFL/aGJQcfpJ9LgV4pCM2kvqkmZzp72jEFfHYmOR6cQK53MX\nbs3yXHtokJUAlYNeUb56qJFX\n-----END PRIVATE KEY-----\n",
            "client_email": "firebase-adminsdk-51hcl@standard-pizzeria.iam.gserviceaccount.com",
            "client_id": "108134239774488478774",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-51hcl%40standard-pizzeria.iam.gserviceaccount.com"
        })

        global firebase_app
        firebase_app = firebase_admin.initialize_app(cred2)
