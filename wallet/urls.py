from django.urls import path

from . import views

app_name = "wallet"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("add/", views.add, name="add"),
    path("edit/<int:transaction_id>/", views.edit, name="edit"),
    path("delete/<int:transaction_id>/", views.delete, name="delete"),
    path("store/", views.store, name="store"),
    path("update/<int:transaction_id>", views.update, name="update"),
    path("destroy/<int:transaction_id>", views.destroy, name="destroy"),
]
