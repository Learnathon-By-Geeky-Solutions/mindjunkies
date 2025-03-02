from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/<str:slug>', views.lecture_home, name="lecture_home"),
    path('video/<str:slug>/<str:video_id>',views.lecture_video,name="lecture_video_content"),
    path('pdf/<str:slug>/<str:pdf_id>',views.lecture_pdf,name="lecture_pdf_content"),
    path('create',views.create_lecture,name="create_lecture")
  
]
