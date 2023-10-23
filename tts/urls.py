from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView
from tts.custom_views.ObtainTokenView import CustomTokenObtainPairView
from tts.custom_views.VerifyTokenView import CustomTokenVerifyView
from . import views

app_name = "tts"
urlpatterns = [
    path("api/generate-text-to-voice/", views.get_audio_api, name="generate-text-to-voice"),

    path("create-token/", CustomTokenObtainPairView.as_view(), name='generate-token'),
    path("refresh-token/", TokenRefreshView.as_view(), name='refresh-token'),
    path("verify-token/", CustomTokenVerifyView.as_view(), name='verify-token'),
]
