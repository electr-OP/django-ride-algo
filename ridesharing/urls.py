"""
URL configuration for ridesharing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger UI
schema_view = get_schema_view(
    openapi.Info(
        title="Ride Sharing Algorithm API",
        default_version="v1",
        description="API documentation for the ride-sharing Algorithm",
        terms_of_service="https://www.ridesharing.com/terms/",
        contact=openapi.Contact(email="support@ridesharing.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
# URL patterns
urlpatterns = [
    # Swagger UI
    path(
        "swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-ui"),
    # Admin URL
    path("admin/", admin.site.urls),
    # API URLs
    path("api/ride/", include("RideRequest.urls"), name="ride"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if bool(settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
