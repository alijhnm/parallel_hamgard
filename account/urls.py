from django.urls import path
from .views import LoginView, RegisterView, AccountActivationSuccessful, AccountActivationFailed, AccountActivationSent,\
                   activate, IndexView, EditProfileView,ProfileView, log_out

app_name = 'account'

urlpatterns = [
    path('<int:pk>/', ProfileView.as_view(), name="profile_page"),
    path('index/', IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', log_out, name="logout"),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('signup/account_activation_sent/', AccountActivationSent.as_view(), name='account_activation_sent'),
    path('signup/activate/<uidb64>/<token>/', activate, name='activate'),
    path('signup/activation_successful/', AccountActivationSuccessful.as_view(), name="success"),
    path('signup/activation_failed/', AccountActivationFailed.as_view(), name="failure"),
    path('edit_profile/', EditProfileView.as_view(), name="edit_profile")
]
