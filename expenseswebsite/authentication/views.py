from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
import logging
from smtplib import SMTPException


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# Authentication views.

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # messages.success(request, 'Success!')
        # messages.warning(request, 'Warning!')
        # messages.info(request, 'Info!')
        # messages.error(request, 'Error!')        

        # Get User Data
        usernameInput = request.POST['username']
        emailInput = request.POST['email']
        passwordInput = request.POST['password']


        context ={
            'fieldValues': request.POST
        }

        # Validate 
        if not User.objects.filter(username=usernameInput).exists():
            if not User.objects.filter(email=emailInput).exists():
                if len(passwordInput) < 6:
                    messages.error(request, 'Password too short.')
                    return render(request, 'authentication/register.html', context)
                
                # Create a user account
                user = User.objects.create_user(username=usernameInput, email=emailInput)
                user.set_password(passwordInput)
                user.is_active = False
                user.save()

                # Send confirmation email
                email_subject = 'Activate your account'
                email_body = 'Please activate your account.'

                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@expenseswebsite.com',
                    [emailInput]
                )

                ''' Option W/O Logging '''
                email.send(fail_silently=False)

                

                messages.success(request, 'User registered successfully.')
                return render(request, 'authentication/register.html')
            else:
                print("User exisrs")
        else:
            print("User already registered with username in the system.")

        

        return render(request, 'authentication/register.html')
    
class UsernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        print("data here")
        print(data)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should contain only alphanumeric characters.'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Username already in use. Choose another one.'},status=409)
        return JsonResponse({'username_valid':True})

class EmailValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        emailInput = data['email']

        if not validate_email(emailInput):
            return JsonResponse({'email_error': 'Email is invalid.'},status=400)
        if User.objects.filter(email=emailInput).exists():
            return JsonResponse({'email_error': 'Email already in use. Choose another one.'},status=409)
        return JsonResponse({'email_valid':True})