from .views import RegistrationView, UsernameValidationView, EmailValidationView, VerificationView, LoginView, LogoutView, RequestPasswordResetEmail, CompletePasswordReset
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', RegistrationView.as_view(), name='registerUrl'),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name='validateUsernameUrl'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validateEmailUrl'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activateUrl'),
    path('login', LoginView.as_view(), name='loginUrl'),
    path('logout', LogoutView.as_view(), name='logoutUrl'),
    path('request-reset-link', RequestPasswordResetEmail.as_view(), name='requestPasswordUrl'),
    path('set-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name='resetPasswordUrl')
]