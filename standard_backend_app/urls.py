# pages/urls.py
from django.urls import path

from pandras_homepage.views import TestHomePage
from django.contrib import admin

from . import views
from .views import get_working_hours, list_categories, create_user, makeorder, list_user_orders, \
    list_users, list_products, list_product_prices, list_products_from_db, get_tamanho_id_from_ped_prod, \
    list_tamanho_from_db

urlpatterns = [
    # path('', homePageView, name='home'),
    path('item_chagelist', views.ItemListView.as_view(), name='item_changelist'),
    path('add_item/', views.ItemCreateView.as_view(), name='add_item'),
    path('<int:pk>/', views.ItemUpdateView.as_view(), name='item_change'),
    path('get_working_hours/', get_working_hours, name='working_hours'),
    path('list_categories/', list_categories, name='list_categories'),
    path('list_product_prices/', list_product_prices, name='list_product_prices'),
    path('list_products_from_db/', list_products_from_db, name='list_products_from_db'),
    path('list_tamanho_from_db/', list_tamanho_from_db, name='list_tamanho_from_db'),
    path('get_tamanho_id_from_ped_prod/', get_tamanho_id_from_ped_prod, name='get_tamanho_id_from_ped_prod'),
    path('create_user/', create_user, name='create_user'),
    path('makeorder/', makeorder, name='makeorder'),
    path('list_user_orders/', list_user_orders, name='list_user_orders'),
    path('list_users/', list_users, name='list_users'),
    path('list_products/', list_products, name='list_products'),
]