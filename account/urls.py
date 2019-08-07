from django.urls import path
from .views import signup, RegisterView

app_name = 'account'
urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup')
]
