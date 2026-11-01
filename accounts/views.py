from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.shortcuts import render, redirect

from languages.models import Language
from .forms import RegistrationForm
from .models import LearnerProfile


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = "core:home"


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            LearnerProfile.objects.create(user=user)

            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend",
            )

            messages.success(
                request,
                "Welcome to NaijaLingua! Your account has been created.",
            )

            return redirect("accounts:dashboard")

    else:
        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


@login_required
def dashboard(request):
    profile, created = LearnerProfile.objects.get_or_create(
        user=request.user
    )

    languages = Language.objects.filter(is_active=True)

    context = {
        "profile": profile,
        "languages": languages,
    }

    return render(
        request,
        "accounts/dashboard.html",
        context,
    )