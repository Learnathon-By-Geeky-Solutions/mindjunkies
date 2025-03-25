from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from mindjunkies.courses.views import category_courses

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mindjunkies.home.urls")),
    path("accounts/", include("mindjunkies.accounts.urls")),
    path("courses/", include("mindjunkies.courses.urls")),
    path("dashboard/", include("mindjunkies.dashboard.urls")),
    path("live_classes/", include("mindjunkies.live_classes.urls")),
    path("category/<slug:slug>/", category_courses, name="category_courses"),
    path("payment/", include("mindjunkies.payments.urls")),
    path("forums/",include("mindjunkies.forums.urls"))
]

if settings.DEBUG:
    urlpatterns += (path("__reload__/", include("django_browser_reload.urls")),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
