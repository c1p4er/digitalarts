"""sokoMarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static  import static

# edit the admin
admin.site.site_header = 'Nickson Auto Services LTD'
admin.site.site_title = 'Nickson Auto Services LTD'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-login/', admin.site.login, name='admin_login'),
    path('', include('pages.urls')), # new  
    path('store/', include('store.urls')), # new
    path('cart', include('carts.urls')), # new
    path('accounts/', include('accounts.urls')), # new
    path('orders/', include('orders.urls')), # new
    path('appointment/', include('appointment.urls')), # new
    path('supplier/', include('supplier.urls')), # new
    path('feedback/', include('feedback.urls')), # new
    
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
