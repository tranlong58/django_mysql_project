from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from wallet.models import Transaction


# Xem danh sách tất cả các giao dịch
def read(request):
    transactions = Transaction.objects.all()
    data = [{'id': transaction.id, 'category': transaction.category,
             'amount': transaction.amount, 'detail': transaction.detail, 'date_created': transaction.date_created} for transaction in transactions]
    return JsonResponse({'transactions': data})


# Tạo một giao dịch mới
@csrf_exempt
def create(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        detail = request.POST.get('detail')
        date_created = request.POST.get('date_created')

        new_transaction = Transaction(
            category=category, amount=amount, detail=detail, date_created=date_created)
        new_transaction.save()

        return JsonResponse({'message': 'Transaction created successfully'})
    else:
        return JsonResponse({'error': 'POST request required'})


# Xem chi tiết một giao dịch
def read_by_id(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    data = {'id': transaction.id, 'category': transaction.category,
            'amount': transaction.amount, 'detail': transaction.detail, 'date_created': transaction.date_created}
    return JsonResponse(data)


# Cập nhật thông tin một giao dịch
@csrf_exempt
def update(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        transaction = get_object_or_404(Transaction, pk=id)
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        detail = request.POST.get('detail')
        date_created = request.POST.get('date_created')

        transaction.category = category
        transaction.amount = amount
        transaction.detail = detail
        transaction.date_created = date_created

        transaction.save()
        return JsonResponse({'message': 'Transaction updated successfully'})
    else:
        return JsonResponse({'error': 'POST request required'})


# Xóa một giao dịch
@csrf_exempt
def delete(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        transaction = get_object_or_404(Transaction, pk=id)
        transaction.delete()
        return JsonResponse({'message': 'Transaction deleted successfully'})
    else:
        return JsonResponse({'error': 'POST request required'})
