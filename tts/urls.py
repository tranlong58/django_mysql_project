from django.urls import path

from tts.views.LoginView import LoginView
from .views import api_view

app_name = "tts"
urlpatterns = [
    path("generate-text-to-voice/", api_view.get_audio_api, name="generate-text-to-voice"),
    path("login/", LoginView.as_view(), name='login'),
]
