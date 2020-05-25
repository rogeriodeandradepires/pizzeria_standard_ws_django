# pages/urls.py
from django.urls import path

from .views import homePageView, get_working_hours, list_categories, create_user, makeorder, list_user_orders, \
    list_users, list_products

urlpatterns = [
    path('', homePageView, name='home'),
    path('get_working_hours/', get_working_hours, name='working_hours'),
    path('list_categories/', list_categories, name='list_categories'),
    path('create_user/', create_user, name='create_user'),
    path('makeorder/', makeorder, name='makeorder'),
    path('list_user_orders/', list_user_orders, name='list_user_orders'),
    path('list_users/', list_users, name='list_users'),
    path('list_products/', list_products, name='list_products'),
]