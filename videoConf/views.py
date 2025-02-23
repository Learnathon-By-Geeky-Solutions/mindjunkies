from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings
import time


# Create your views here.
@require_http_methods(["GET"])
@login_required
def meeting(request: HttpRequest) -> HttpResponse:

    

    context = { 
        'room_name': 'room is awesome',
        'JITSI_MAGIC_COOKIE': settings.JITSI_MAGIC_COOKIE,
        'SRI_HASH': settings.SRI_HASH,
        'display_name': 'anonymous',
        'jwt': settings.JWT,
        }

    return render(request, "meet/index.html", context)
