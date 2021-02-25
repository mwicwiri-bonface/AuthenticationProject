from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import (NoReverseMatch)
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import View
from .forms import UserSignupForm, UserUpdateForm, ProfileUpdateForm
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .models import CustomUser
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages


# Sign Up View
class SignUpView(View):
    form_class = UserSignupForm
    template_name = 'accounts/sign-up.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate your  interview-django-login-app account'
            message = render_to_string('emails/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, 'Please Confirm your email to complete registration.')

            return redirect('accounts:login')

        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            auth_login(request, user)
            messages.success(request, 'Your account have been confirmed.')
            return redirect('home:home')
        else:
            messages.warning(request, 'The confirmation link was invalid, possibly because it has already been used.')
            return redirect('home:home')


def user_login(request):
    if request.method == "POST":
        remember = request.POST.get('remember')
        username = request.POST.get('login-email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if remember != "remember-me":
            request.session.set_expiry(0)
        if user is not None:
            if user.is_active and not user.is_archive:
                auth_login(request, user)
                user_name = request.user.get_full_name
                messages.success(request, f"Hi {user_name}, welcome to home page.")
                try:
                    return redirect(request.GET.get('next', ''))
                except (NoReverseMatch, ImproperlyConfigured):
                    return redirect("home:home")
            else:
                logout(request)
                messages.warning(request, "sorry, your account is inactive")
                try:
                    return redirect(request.GET.get('next', ''))
                except (NoReverseMatch, ImproperlyConfigured):
                    return redirect("accounts:login")
        else:
            messages.warning(request, "please check, your email or password is incorrect.")
            try:
                return redirect(request.GET.get('next', ''))
            except (NoReverseMatch, ImproperlyConfigured):
                return redirect("accounts:login")
    return render(request, 'accounts/login.html')


@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your Profile has been updated!')
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user)
        u_form = UserUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form,
        'u_form': u_form
    }
    return render(request, 'home/profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:change-password')
        else:
            messages.info(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'home/change-password.html', context)
