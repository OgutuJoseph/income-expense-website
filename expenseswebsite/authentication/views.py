from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
import logging
from smtplib import SMTPException

from django.urls import reverse
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator


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

                ## path_to_view
                ### - getting the domain we're on
                domain  = get_current_site(request).domain

                ### - encode uid
                ### - token
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                ### - relative url for verification (reset password)
                link = reverse('activateUrl', kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})
                activate_url = 'http://'+domain+link
                
                # Send confirmation email
                email_subject = 'Zen :: Activate Your Account'
                email_body = 'Hi ' + user.username + '. Please use this link to verify your account. \n' + activate_url

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
                print("User exists.")
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

class VerificationView(View):
    def get(self, request, uidb64, token):


        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            # if token is not valid, meaning has already been used
            if not token_generator.check_token(user, token):
                return redirect('loginUrl'+'?message='+'User already activated')

            # if user is not yet active, activate user, else route to login
            if user.is_active:
                return redirect('loginUrl')            
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully.')
            return redirect('loginUrl')

        except Exception as ex:
            pass

        return redirect('loginUrl')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        usernameInput = request.POST['username']
        passwordInput = request.POST['password']

        if usernameInput and passwordInput:
            user = auth.authenticate(username=usernameInput, password=passwordInput)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username + '. ' + 'You are now logged in.')
                    return redirect('expensesUrl')

                messages.error(request, 'Account is not active. Please check your mailbox for account activation email.')
                return render(request, 'authentication/login.html')

            messages.error(request, 'Invalid login credentials. Try again or register a new account.')
            return render(request, 'authentication/login.html')

        messages.error(request, 'Please provide both username and password before logging in.')
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('loginUrl')

class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')
    
    def post(self, request):
        emailInput = request.POST['email']
        context = {
            'values': request.POST
        }

        if not validate_email(emailInput):
            messages.error(request, 'Please supply a valid email.')
            return render(request, 'authentication/reset-password.html', context)

        current_site = get_current_site(request)
        user = User.objects.filter(email=emailInput)
        if user.exists():
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0])
            }
            link = reverse('resetPasswordUrl', kwargs={'uidb64':email_contents['uid'], 'token':email_contents['token']})
            email_subject = 'Zen :: Password Reset Instructions'
            reset_url  = 'http://'+current_site.domain+link
            email = EmailMessage(
                    email_subject,
                    'Hi there, please use the link below to complete resettting your password: \n' + reset_url,
                    'noreply@expenseswebsite.com',
                    [emailInput]
                )
            email.send(fail_silently=False)
            messages.success(request, 'We have sent you an emal with password reset link.')


        messages.success(request, 'We have sent you an emal with password reset link.')

class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Password reset token invlid. Please generate a new one.')             
                return render(request, 'authentication/reset-password.html', context)
        except Exception as ex:
            pass

        return render(request, 'authentication/set-newpassword.html', context)
    
    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        passwordInput = request.POST['password']
        passwordInput2 = request.POST['password2']

        if passwordInput != passwordInput2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authentication/set-newpassword.html', context)

        if len(passwordInput) < 6:
            messages.error(request, 'Password to short')
            return render(request, 'authentication/set-newpassword.html', context)
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(passwordInput)
            user.save()
            messages.success(request, 'Password reset successfully. Proceed to login')
            return redirect('loginUrl')    
        except Exception as ex:
            messages.info(request, 'Something went wrong. Try again.')
            return render(request, 'authentication/set-newpassword.html', context)

        