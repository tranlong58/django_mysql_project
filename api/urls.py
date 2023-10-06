from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path("transaction/create/", views.create, name="create"),
    path("transaction/read/", views.read, name="read"),
    path("transaction/update/", views.update, name="update"),
    path("transaction/delete/", views.delete, name="delete"),
    path("transaction/read/<int:transaction_id>/",
         views.read_by_id, name="read_by_id"),
]
