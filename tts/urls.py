from django.urls import path
from tts.views import CustomTokenObtainPairView, CustomTokenVerifyView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views

app_name = "tts"
urlpatterns = [
    path("", views.index, name="index"),
    path("result/", views.result, name="result"),
    path("solve/", views.solve, name="solve"),
    path("api/generate-text-to-voice/", views.get_audio_api, name="generate-text-to-voice"),
    # path("create-token/", views.create_token, name="create-token"),
    path("create-token/", CustomTokenObtainPairView.as_view(), name='generate-token'),
    path("refresh-token/", TokenRefreshView.as_view(), name='refresh-token'),
    path("verify-token/", CustomTokenVerifyView.as_view(), name='verify-token'),
]
