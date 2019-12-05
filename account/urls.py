from django.urls import path

from account.views import (
    ActivateAccountView,
    RegisterView,
    SubscribeToNewsletterView,
    VerificationSentView,
)


urlpatterns = [
    path('activate/<slug:uidb64>/<slug:token>/', ActivateAccountView.as_view(), name='activate'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verification-sent/', VerificationSentView.as_view(), name='verification-sent'),
    path(
        'subscribe-to-newsletter/<slug:uidb64>/',
        SubscribeToNewsletterView.as_view(), name='subscribe-to-newsletter'
    ),
]
