from accounts.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions


class Login(APIView):

    def post(self, request):
        phone_number = request.data.get('phone_number')
        opt = request.data.get('otp')
        user = User.objects.get_or_create(phone_number=phone_number)
        token, _ = Token.objects.get_or_create(user=user[0])
        return Response({'token': token.key}, status=status.HTTP_200_OK)
        