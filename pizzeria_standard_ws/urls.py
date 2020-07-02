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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from pandras_homepage.admin import pandras_admin_site
from pizzeria_standard_ws import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('admin/standard_backend_app/pedido/<str:pk>/', admin.site.urls),
    path('pandras-admin/', pandras_admin_site.urls),
    path('', include('pandras_homepage.urls')),
    path('', include('standard_backend_app.urls')),
    path('get_working_hours/', include('standard_backend_app.urls')),
    path('list_categories/', include('standard_backend_app.urls')),
    path('list_product_prices/', include('standard_backend_app.urls')),
    path('list_products_from_db/', include('standard_backend_app.urls')),
    path('list_tamanho_from_db/', include('standard_backend_app.urls')),
    path('get_tamanho_id_from_ped_prod/', include('standard_backend_app.urls')),
    path('create_user/', include('standard_backend_app.urls')),
    path('makeorder/', include('standard_backend_app.urls')),
    path('list_user_orders/', include('standard_backend_app.urls')),
    path('list_users/', include('standard_backend_app.urls')),
    path('list_products/', include('standard_backend_app.urls')),
    path('item_chagelist/', include('standard_backend_app.urls')),
    path('add_item/', include('standard_backend_app.urls')),
    path('<int:pk>/', include('standard_backend_app.urls')),

    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.STATICFILES_DIRS, document_root=settings.STATICFILES_DIRS)
# urlpatterns += static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
