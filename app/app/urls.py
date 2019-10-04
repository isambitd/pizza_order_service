from django.contrib import admin
from django.urls import path, include

from django.contrib.auth.models import User
from api.models import Pizza, Order, Customer
from rest_framework import routers

from api.views import CustomerViewSet, OrderViewSet, PizzaViewSet

router = routers.DefaultRouter()
router.register(r'api/customers', CustomerViewSet)

router.register(r'api/orders', OrderViewSet)

router.register(r'api/pizzas', PizzaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', include(router.urls)),
    path(r'api/', include('rest_framework.urls', namespace='rest_framework'))

]
