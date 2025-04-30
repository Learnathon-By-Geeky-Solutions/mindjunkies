from django.urls import path

from .views import HomeView, search_view, proxy_pdf

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("search/results/", search_view, name="search_view"),
    path("proxy/", proxy_pdf, name="proxy_pdf"),
]
