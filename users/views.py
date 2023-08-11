from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
import jwt

from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from users.serializers import RegisterSerializer, LoginSerializer
from users.utils import Util

class RegisterView(generics.GenericAPIView):
    """
    Register a new user.
    """
    serializer_class = RegisterSerializer

    def post(self, request):
        """
        Register a new user.
        """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        email_body = f'Hi {user.username}, Use this link to verify your email:\n{absurl}'
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(APIView):
    """
    Verify user's email address using a token.
    """
    def get(self, request):
        """
        Verify user's email address using a token.
        """
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    """
    User login.
    """
    serializer_class = LoginSerializer

    def post(self, request):
        """
        User login.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
