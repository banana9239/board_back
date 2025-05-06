from time import sleep
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ParseError, NotFound
from rest_framework import status
from . import serializers
import requests
from config import settings
from .models import User


class Me(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        serializer = serializers.UserDetailSerializer(request.user)
        return Response(serializer.data)
        
        
    def put(self, request):
        #데이터를 가져와서
        user = request.user
        #여기에 적용하고 데이터가 적합한지를 if를 통해 검사한다.
        serializer = serializers.UserDetailSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            #검사가 통과되면 그대로 저장
            user = serializer.save()
            serializer = serializers.UserDetailSerializer(user)
            return Response(serializer.data)
        else:
            
            return Response(serializer.errors)


class Users(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError("Password is required.")
        serializer = serializers.UserDetailSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.UserDetailSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)



class LogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError("잘못된 입력입니다.")
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user:
            login(request, user)
            return Response({"ok":"Welcome!"})
        else:
            return Response(
                {"error":"wrong password"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class LogOut(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sleep(5)
        logout(request)
        return Response({"ok":"Goodbye!"})
    
    
class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({"ok":"Password changed."})
        else:
            raise ParseError("Wrong password.")
        
class Github(APIView):

    def post(self, request):
        try:
            code = request.data.get("code")
            if not code:
                raise ParseError("No code.")
            access_token = requests.post(f"https://github.com/login/oauth/access_token?code={code}&client_id=Ov23liduaLQ9hsV8PA29&client_secret={settings.GH_SECRET}",
                                        headers={"Accept":"application/json"})
            access_token = access_token.json().get("access_token")

            user = requests.get("https://api.github.com/user",
                                headers={
                                    "Authorization":f"Bearer {access_token}",
                                    "Accept":"application/json"
                                })
            
            user_email = requests.get("https://api.github.com/user/emails",
                                headers={
                                    "Authorization":f"Bearer {access_token}",
                                    "Accept":"application/json"
                                })
            user_email = user_email.json()[0]['email']
            try:
                user = User.objects.get(email=user_email)
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    email=user_email,
                    username=user.json().get("login"),
                    name=user.json().get("name"),
                    nickname=user.json().get("login"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            raise Response(status=status.HTTP_400_BAD_REQUEST)
        
class CheckUsername(APIView):
    def post(self, request):
        username = request.data.get("username")
        if not username:
            raise ParseError("No username.")
        try:
            User.objects.get(username=username)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_200_OK)