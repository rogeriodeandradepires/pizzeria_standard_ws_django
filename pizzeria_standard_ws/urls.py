"""pizzeria_standard_ws URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('standard_backend_app.urls')),
    path('get_working_hours/', include('standard_backend_app.urls')),
    path('list_categories/', include('standard_backend_app.urls')),
    path('create_user/', include('standard_backend_app.urls')),
    path('makeorder/', include('standard_backend_app.urls')),
    path('list_user_orders/', include('standard_backend_app.urls')),
    path('list_users/', include('standard_backend_app.urls')),
    path('list_products/', include('standard_backend_app.urls')),
]
