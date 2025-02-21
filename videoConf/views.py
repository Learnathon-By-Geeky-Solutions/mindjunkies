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
        'room_name': f"{settings.JITSI_ROOM_PREFIX}{request.user.name}_{int(time.time())}",
        'user_name': request.user.username,
        'JITSI_MAGIC_COOKIE': settings.JITSI_MAGIC_COOKIE,
        'SRI_HASH': settings.SRI_HASH,
        }
    
    response = render(request, 'meet/index.html', context)
    response['Content-Security-Policy'] = "frame-ancestors 'self' 8x8.vc"
    response['X-Frame-Options'] = 'SAMEORIGIN'
    
    return response