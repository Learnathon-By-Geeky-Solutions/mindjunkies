from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings
urlpatterns=[
    path('home',views.lecture_home ,name="lecture_home"),
    path('create_lecture',views.create_lecture,name="create_lecture")
]