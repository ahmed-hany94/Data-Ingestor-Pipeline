from django.contrib import admin
from django.urls import include, path
 
from transactions.views import healthz

urlpatterns = [
    path('admin/', admin.site.urls),
    path("healthz", healthz),
    path("api/", include("transactions.urls")),
]
