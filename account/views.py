from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.viewsets import  GenericViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from account.serializers import RegisterSerializer, UserListSerializer, UserDetailSerializer
from account.serializers import LoginSerializer

# Create your views here.

class UserRegistration(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('account create succsessful', status=200)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]

class CustomViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,GenericViewSet):
    pass

class UserViewSet(CustomViewSet):
    queryset = User.objects.all()
    def get_serializer_class(self):
        if self.action =='retrieve':
            return UserDetailSerializer
        return UserListSerializer

    def get_permissions(self):
        if self.request.method == 'retrieve':
            return IsAdminUser(),
        return IsAuthenticated,


class LoginView(ObtainAuthToken):

    serializer_class = LoginSerializer


    def post(self, request):
        serializer = self.serializer_class(data = request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user)
        print(user)
        response_data = {
            'token': token.key,
            'username': user.username,
            'id': user.id
        }
        return Response(response_data)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('you are go out from your account')