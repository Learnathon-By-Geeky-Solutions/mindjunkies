from django.urls import path

from .views import HomeView, search_view

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("search/results/", search_view, name="search_view"),
]
