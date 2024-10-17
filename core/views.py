from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import User, Wallet, Transaction

@login_required
def send_money(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        transaction = Transaction(sender=request.user, receiver=receiver, amount=amount)
        if transaction.process_transaction():
            return redirect('success_page')  # Redirige vers une page de succès
        else:
            return render(request, 'send_money.html', {'error': 'Solde insuffisant'})
    return render(request, 'send_money.html', {'receiver': receiver})
