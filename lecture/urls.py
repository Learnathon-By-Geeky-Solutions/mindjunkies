from django.urls import path
from . import views 

urlpatterns=[
    path('home',views.lecture_home ,name="lecture_home"),
    path('create_lecture',views.create_lecture,name="create_lecture")
]