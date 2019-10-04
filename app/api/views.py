from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from .serializers import PizzaSerializer, CustomerSerializer, OrderSerializer, ItemSerializer
from .models import Customer, Pizza, Order, Item
from rest_framework import generics


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        status = self.request.query_params.get("status")
        customer = self.request.query_params.get("customer")
        queryset = Order.objects.all()
        if status:
            queryset = Order.objects.filter(status=status)
        if customer:
            queryset = Order.objects.filter(customer=customer)
        return queryset


# class ItemViewSet(viewsets.ModelViewSet):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer
