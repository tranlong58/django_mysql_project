from django.urls import path

from . import views

app_name = "tts"
urlpatterns = [
    path("", views.index, name="index"),
    path("result/", views.result, name="result"),
    path("solve/", views.solve, name="solve"),
    path("api/get_audio/", views.get_audio_api, name="get_audio_api"),
    path("create_token/", views.create_token, name="create_token"),
]
