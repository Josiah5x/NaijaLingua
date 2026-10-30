from django.shortcuts import render
from languages.models import Language


def home(request):
    languages = Language.objects.filter(is_active=True)

    context = {
        "languages": languages,
    }

    return render(request, "core/home.html", context)