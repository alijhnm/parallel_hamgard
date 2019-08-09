from django.urls import path
from .views import LoginView, RegisterView, AccountActivationSuccessful, AccountActivationFailed, AccountActivationSent,\
                   activate, IndexView

app_name = 'account'
urlpatterns = [
    path('index/', IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('signup/account_activation_sent/', AccountActivationSent, name='account_activation_sent'),
    path('signup/activate/<uidb64>/<token>/', activate, name='activate'),
    path('signup/activation_successful/', AccountActivationSuccessful.as_view(), name="success"),
    path('signup/activation_failed/', AccountActivationFailed.as_view(), name="failure")
]
