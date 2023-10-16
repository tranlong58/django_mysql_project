from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path("create/", views.create, name="create"),
    path("read/", views.read, name="read"),
    path("update/", views.update, name="update"),
    path("delete/", views.delete, name="delete"),
    path("read/<int:transaction_id>/", views.read_by_id, name="read_by_id"),
]
