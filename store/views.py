from django.shortcuts import render
from store.serializers import StoreSerializer, ProductSerializer, CategorySerializer
from store.models import Category, Store, Product
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions

# Create your views here.


class StoreView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, id):
        store = Store.objects.get(id=id)
        serializer = StoreSerializer(store)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def post(self, request):

        name = request.data.get('name')
        address = request.data.get('address')
        user = request.user
        serializer = StoreSerializer(
            data={"name": name, "address": address}, context={"user": request.user})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)


class ProductView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, id):
        store = Store.objects.get(id=id)
        products = Product.objects.filter(store=store)
        group_by = {}

        for i in products:
            if(i.category):
                if(not group_by.get(i.category.name)):
                    group_by[i.category.name] = [ProductSerializer(i).data]
                group_by[i.category.name].append(ProductSerializer(i).data)
        print(group_by)
        return Response(group_by, status=status.HTTP_200_OK)

    def post(self, request, id):
        request.data['store'] = id
        category, is_created = Category.objects.get_or_create(
            name=request.data.get('category'))
        request.data['category'] = category.id
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            s_data = serializer.data
            data = {
                "name": s_data['name'],
                'id': s_data['id'],
                'image': s_data['image']
            }
            return Response(
                data,
                status=status.HTTP_201_CREATED,
            )
        return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
