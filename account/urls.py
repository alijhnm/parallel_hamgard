from django.urls import path
from .views import *

app_name = 'account'
urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('signup/account_activation_sent/', AccountActivationSent, name='account_activation_sent'),
    path('signup/activate/<uidb64>/<token>/', activate, name='activate'),
    path('signup/activation_successful/', AccountActivationSuccessful.as_view(), name="success"),
    path('signup/activation_failed/', AccountActivationFailed.as_view(), name="failure")
]
