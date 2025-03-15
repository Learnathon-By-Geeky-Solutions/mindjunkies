from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/results/", views.search_results, name="search_results"),
]
