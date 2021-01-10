from django.shortcuts import render
from store.serializers import StoreSerializer, ProductSerializer, CategorySerializer
from store.models import Category, Store, Product
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from django.db.models import Sum


# Create your views here.

class CartView(APIView):
    """
        Creates a cart. User not needed.
    """

    def get(self, request):
        pass

    def post(self, request):
        cart = Cart.objects.create()
        return Response({"id": cart.id}, status=status.HTTP_201_CREATED)


class CartItemView(APIView):
    """
        Adds and Removes an item from the cart
    """

    def post(self, request, id):
        store = request.data.get('storeLink')
        quantity = request.data.get('quantity')
        product_id = request.data.get('product_id')

        product = Product.objects.get(id=product_id)

        total_item_cost = quantity * product.sale_price

        cart = Cart.objects.get(id=id)
        cart_item = CartItem.objects.create(
            product=product, cart=cart, quantity=quantity, total=total_item_cost)

        total_cart_item = CartItem.objects.filter(
            cart=id).aggregate(Sum('total'))

        cart.total = total_cart_item['total__sum']
        cart.save()

        return Response('success', status=status.HTTP_200_OK)

    def delete(self, request, id):
        cart_item = CartItem.objects.delete(id=id)

        return Response('', status=status.HTTP_200_OK)


class CartCheckout(APIView):
    """
       Checkout endpoint. User should be authenticated or pass a phone_number and otp to create a new user. 
    """
    authentication_classes = [TokenAuthentication]

    def post(self, request, id):
        customer = request.user

        if(customer.is_anonymous):
            phone = request.data.get('phone_number')
            otp = request.data.get('otp')

            if(phone and otp):
                customer = User.objects.create(phone_number=phone_number)
            else:
                return Response('No user found please enter your mobile number and otp', status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.get(id=id)
        order = Order.objects.create(customer=customer, total=cart.total)

        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            order_item = OrderItem.objects.create(
                order=order, product=item.product, total=item.total)
            cart_items.delete()

        cart.delete()

        return Response({"order_id": order.id}, status=status.HTTP_200_OK)
