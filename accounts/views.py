from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PasswordChangeForm
from django.conf import settings
import pandas as pd
import os

from django.contrib.auth.forms import PasswordResetForm

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import ForgotPasswordForm

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")

    return render(request, "accounts/login.html")





@login_required
def change_password_view(request):

    if request.method == 'POST':

        form = PasswordChangeForm(request.POST)

        if form.is_valid():

            new_password = form.cleaned_data['new_password']

            request.user.set_password(new_password)
            request.user.save()

            file_path = os.path.join(
                settings.BASE_DIR,
                'media',
                'users.xlsx'
            )

            df = pd.read_excel(file_path)

            df.loc[
                df['username'] == request.user.username,
                'password'
            ] = new_password

            df.to_excel(file_path, index=False)

            return redirect('login')

    else:
        form = PasswordChangeForm()

    return render(
        request,
        'accounts/change_password.html',
        {'form': form}
    )



User = get_user_model()


def forgot_password_view(request):

    form = PasswordResetForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            form.save(
                request=request,
                use_https=True,
                email_template_name="accounts/password_reset_email.html"
            )
            return redirect("password_reset_done")

    return render(request, "accounts/forgot_password.html", {"form": form})

@login_required
def profile_view(request):

    return render(
        request,
        'accounts/profile.html',
        {
            'user': request.user
        }
    )

def logout_view(request):
    logout(request)
    return redirect("login")