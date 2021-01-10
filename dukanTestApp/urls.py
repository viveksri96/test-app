"""dukanTestApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import Login
from accounts.admin import my_admin_site
from store.views import StoreView, ProductView
from cart.views import CartView, CartItemView, CartCheckout

urlpatterns = [
    path('v1/admin/', my_admin_site.urls),
    path('v1/login/', Login.as_view()),
    path('v1/store/<int:id>/', StoreView.as_view()),
    path('v1/store/', StoreView.as_view()),
    path('v1/store/<int:id>/product/', ProductView.as_view()),
    path('v1/cart/', CartView.as_view()),
    path('v1/cart/<int:id>/', CartItemView.as_view()),
    path('v1/cart/<int:id>/checkout/', CartCheckout.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
