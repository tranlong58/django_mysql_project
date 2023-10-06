from django.urls import path

from . import views

app_name = "tts"
urlpatterns = [
    path("", views.index, name="index"),
    path("result/", views.result, name="result"),
    path("solve/", views.solve, name="solve"),
]
