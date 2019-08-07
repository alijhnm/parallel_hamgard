from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from .models import User
from .forms import RegisterForm


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
            user.save()

            # Login the user
            login(self.request, user)
            return HttpResponseRedirect("www.google.com")


def signup(request):
    # if this is a POST request we need to process the form data
    template = 'account/register.html'

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone_number = form.cleaned_data['phone_number']
                user.save()

                # Login the user
                login(request, user)

                # redirect to accounts page:
                return HttpResponseRedirect('/mymodule/account')

    # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})
