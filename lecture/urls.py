from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings
urlpatterns=[
    path('home',views.lecture_home ,name="lecture_home"),
    path('create_topic',views.create_content,name="create_content"),
    path('create_lecture',views.create_module,name="create_module")
]