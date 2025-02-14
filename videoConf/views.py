from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def meeting(request: HttpRequest) -> HttpResponse:
    return render(request, 'meet/index.html')