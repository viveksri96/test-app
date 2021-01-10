from django.shortcuts import render
from store.serializers import StoreSerializer, ProductSerializer, CategorySerializer
from store.models import Category, Store, Product
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions


# Create your views here.

class OrderView(APIView):

    def get(self, request):
        pass
