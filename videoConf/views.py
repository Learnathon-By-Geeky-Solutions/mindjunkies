from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings


# Create your views here.
@require_http_methods(["GET"])
@login_required
def meeting(request: HttpRequest) -> HttpResponse:
    context = { 
        'room_name': 'life is beautiful',
        'user_name': 'user_name',
        'JITSI_MAGIC_COOKIE': settings.JITSI_MAGIC_COOKIE
        }
    
    response = render(request, 'meet/index.html', context)
    response['Content-Security-Policy'] = "frame-ancestors 'self' 8x8.vc"
    response['X-Frame-Options'] = 'SAMEORIGIN'
    
    return response