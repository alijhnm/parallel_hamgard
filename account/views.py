from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, TemplateView, DetailView, View

from account.tokens import account_activation_token
from .models import User, Profile
from .forms import RegisterForm, LoginForm, EditProfileForm
from .utils import send_html_mail
from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(View):

    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())


class IndexView(TemplateView):
    template_name = "account/index.html"


class HomeView(TemplateView):
    template_name = "account/home.html"


class ProfileView(DetailView):
    template_name = "account/profile.html"
    model = Profile

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        obj = self.model.objects.get(pk=pk)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.object.user
        return context


class EditProfileView(LoginRequiredMixin, FormView):
    login_required = True
    template_name = "account/profile_edit.html"
    form_class = EditProfileForm

    def form_valid(self, form):

        print(self.kwargs)
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        email = form.cleaned_data["email"]
        phone_number = form.cleaned_data["phone_number"]
        user = self.request.user

        print(user)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone_number
        user.save()

        return HttpResponseRedirect(reverse("account:profile_page", args=(user.profile.pk,)))


class LoginView(FormView):
    template_name = 'account/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
            return HttpResponseRedirect(reverse("account:profile_page", args=(user.profile.pk,)))
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
            user.mobile_number = form.cleaned_data['phone_number']
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
            send_html_mail(subject, message, (user.email,))
            # Login the user
            return HttpResponseRedirect(reverse('account:account_activation_sent'))


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
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_is_verified = True
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse("account:success"))
    else:
        return HttpResponseRedirect(reverse("account:failure"))


@require_http_methods(["POST", "GET"])
def log_out(request):
    user = request.user
    if user:
        logout(request)
    else:
        print("Failed")
    return HttpResponseRedirect(reverse('home'))

