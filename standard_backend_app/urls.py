# pages/urls.py
from django.urls import path

from .views import homePageView, get_working_hours, list_categories

urlpatterns = [
    path('', homePageView, name='home'),
    path('get_working_hours/', get_working_hours, name='working_hours'),
    path('list_categories/', list_categories, name='list_categories')
]