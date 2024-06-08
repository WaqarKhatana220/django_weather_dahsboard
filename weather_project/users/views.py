from django.shortcuts import render, redirect
from django.views import View
from .models import User
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class RegisterView(View):
    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_serializer = UserSerializer(data={'email': email, 'password': password})
        if user_serializer.is_valid():
            user_serializer.save()
            return redirect('token_obtain_pair')
        else:
            # Pass validation errors to the template context
            errors = user_serializer.errors
            for field, messages_list in errors.items():
                for message in messages_list:
                    messages.error(request, f"{field}: {message}")
            return render(request, 'users/register.html', {'errors': errors})

class CustomTokenObtainPairView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            # Redirect to the weather endpoint upon successful login
            return redirect('/api/weather/')  # Assuming this is the correct URL for the weather endpoint
        return render(request, 'users/login.html', {'error': 'Invalid email or password'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('token_obtain_pair')