from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import loader

from .models import Transaction


class IndexView(generic.ListView):
    template_name = "transaction/index.html"
    context_object_name = "transaction_list_by_date_created"

    def get_queryset(self):
        """Return the last five published questions."""
        return Transaction.objects.all().order_by("-date_created", "-id")


def add(request):
    return render(request, "transaction/add.html")


def edit(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    return render(request, "transaction/edit.html", {"transaction": transaction})


def delete(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    return render(request, "transaction/delete.html", {"transaction": transaction})


def store(request):
    new_transaction = Transaction(
        category=request.POST["category"],
        amount=request.POST["amount"],
        detail=request.POST["detail"],
        date_created=request.POST["date_created"]
    )
    new_transaction.save()
    return HttpResponseRedirect(reverse("wallet:index"))


def update(request, transaction_id):
    updated_transaction = get_object_or_404(Transaction, pk=transaction_id)

    updated_transaction.category = request.POST["category"]
    updated_transaction.amount = request.POST["amount"]
    updated_transaction.detail = request.POST["detail"]
    updated_transaction.date_created = request.POST["date_created"]

    updated_transaction.save()
    return HttpResponseRedirect(reverse("wallet:index"))


def destroy(request, transaction_id):
    deleted_transaction = get_object_or_404(Transaction, pk=transaction_id)
    deleted_transaction.delete()
    return HttpResponseRedirect(reverse("wallet:index"))
