from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, TemplateView

from account.tokens import account_activation_token
from .models import User
from .forms import RegisterForm, LoginForm
from .utils import send_html_mail


class IndexView(TemplateView):
    template_name = "account/index.html"


class LoginView(FormView):
    template_name = 'account/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)
        if user:
            return HttpResponseRedirect(reverse("account:index"))
        else:
            return render(self.request, self.template_name, {"form": form,
                                                             "error_message": "Invalid username or password"})


class RegisterView(FormView):
    template_name = 'account/register.html'
    form_class = RegisterForm
    success_url = 'www.google.com'

    def form_valid(self, form):
        if User.objects.filter(username=form.cleaned_data['username']).exists():
            return render(self.request, self.template_name, {
                'form': form,
                'error_message': 'Username already exists.'
            })
        elif User.objects.filter(email=form.cleaned_data['email']).exists():
            return render(self.request, self.template_name, {
                'form': form,
                'error_message': 'Email already exists.'
            })
        elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
            return render(self.request, self.template_name, {
                'form': form,
                'error_message': 'Passwords do not match.'
            })
        else:
            user = User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password']
            )
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.phone_number = form.cleaned_data['phone_number']
            user.is_active = False
            user.save()
            current_site = get_current_site(self.request)
            subject = 'Activate Your Hamgard Account'
            message = render_to_string('account/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            print("In Views. Sending email.")
            send_html_mail(subject, message, (user.email,))
            # Login the user
            login(self.request, user)
            return render(self.request, "account/account_activation_sent.html", {})


class AccountActivationSent(TemplateView):
    template_name = "account/account_activation_sent.html"


class AccountActivationSuccessful(TemplateView):
    template_name = "account/account_activation_valid.html"


class AccountActivationFailed(TemplateView):
    template_name = "account/account_activation_invalid.html"


@require_http_methods(["POST", "GET"])
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None
        print(e)
    print(user)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_is_verified = True
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse("account:success"))
    else:
        return HttpResponseRedirect(reverse("account:failure"))


class HomeView(TemplateView):
    template_name = "account/home.html"
