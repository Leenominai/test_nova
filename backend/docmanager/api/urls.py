from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .views import create_google_drive_document


urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("upload/", create_google_drive_document, name="file-upload"),
]