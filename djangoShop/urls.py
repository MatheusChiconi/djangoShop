"""
URL configuration for djangoShop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf.urls.static import static
from core.views import *
from produtos.views import produtos
from django.http import HttpResponse

def placeholder_view(request):
    # utilzar quando quero colocar uma url ainda sem view
    return HttpResponse("Página do catálogo em construção ⚠️")

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('produto/<uuid:codigo>/', produtos, name='produto_detail'),
    path('contas/', include('contas.urls')),
    path('contas/', include('django.contrib.auth.urls')),  # URLs de autenticação padrão do Django

    # Tirar o placeholder_view e colocar a view correta quando estiver pronto
    path('shop/', placeholder_view, name='shop'),
    path('blog/', placeholder_view, name='blog'),
    path('about/', placeholder_view, name='about'),
    path('contact/', placeholder_view, name='contact'),
    path('cart/', placeholder_view, name='cart'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
