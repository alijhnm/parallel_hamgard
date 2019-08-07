import datetime
import binascii
import os
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile_number = models.CharField(max_length=500, blank=True, null=True, default=None)
    email_is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=40, null=True, blank=True)
    remember_me = models.BooleanField(default=False)
    token_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def login_user(self, remember_me):
        now = datetime.date.today()
        self.last_login = now
        if not self.token:  # or self.expired:
            self.token = self.generate_token()
            self.token_created = now
            self.remember_me = remember_me
            self.deleted = False
            self.save()
            return self.token
        else:
            return self.token

    def logout_user(self):
        self.token = None
        self.save()

    @staticmethod
    def generate_token():
        return binascii.hexlify(os.urandom(20)).decode()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)
    bio = models.TextField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.user.username

