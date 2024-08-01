from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User

# Authentication views.

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
class UsernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        print("data here")
        print(data)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should contain alphanumeric characters.'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Username already in use. Choose another one.'},status=409)
        return JsonResponse({'username_valid':True})