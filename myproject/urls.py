from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path("mro/", include("mro.urls")),
    path("tm/", include("tm.urls")),
    path("engineer/", include("engineer.urls")),
    path("head/", include("head.urls")),
]
