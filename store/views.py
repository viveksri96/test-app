from django.shortcuts import render
from store.serializers import StoreSerializer, ProductSerializer, CategorySerializer
from store.models import Category, Store, Product
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from collections import defaultdict
from collections import OrderedDict


class IsAuthenticated(permissions.BasePermission):
    """
        Custom method for authentication
    """
    SAFE_METHODS = ['POST', 'DELETE']

    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS:
            return request.user.is_authenticated
        return True


class StoreView(APIView):
    """
        Creates, retrieve a store
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
    """
        Creates, retrieve and removes a product from store
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        store = Store.objects.get(id=id)
        products = Product.objects.filter(store=store)
        group_by = {}
        category_counter = {}

        for i in products:
            if(i.category):
                if(not group_by.get(i.category.name)):
                    group_by[i.category.name] = [ProductSerializer(i).data]
                    category_counter[i.category.name] = 1
                else:
                    group_by[i.category.name].append(ProductSerializer(i).data)
                    category_counter[i.category.name] += 1

        od_data = OrderedDict()
        for k in sorted(group_by, key=lambda k: len(group_by[k]), reverse=True):
            od_data[k] = group_by[k]
        return Response(od_data, status=status.HTTP_200_OK)

    def post(self, request, id):
        request.data['store'] = id

        store = Store.objects.get(id=id)
        if(not store.owner == request.user):
            return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)

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

    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
            product.delete()
            return Response("", status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response("Product not Found", status=status.HTTP_404_NOT_FOUND)
