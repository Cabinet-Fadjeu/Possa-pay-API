from paypal.standard.models import ST_PP_COMPLETED
from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received
from .models import Transaction
from userAuth.models import CustomUser,Wallet
from decimal import Decimal
from .utils import send_order_notification

@receiver(valid_ipn_received)
def handle_valid_ipn(sender, **kwargs):
    print('pret')
    ipn_obj = sender
    print('recue')
    # Vérifiez si la transaction est un succès
    if ipn_obj.payment_status == "Completed":
        print('reussi')
        # Récupérez la commande correspondant à cette transaction
        try:
            recharge = Transaction.objects.get(id=ipn_obj.invoice, status='Pending')
            print(f"✅ Transaction trouve ! Transaction {recharge} .")
            recharge.status = 'Completed'
            recharge.save()
            #crediter wallet

            amount =recharge.amount
            user=recharge.sender
            sender_wallet = Wallet.objects.get(user_id=user.id)
            sender_wallet.amount += Decimal(amount)
            sender_wallet.save()

            #send_order_notification(order,product)
            print('modifi')
        except Transaction.DoesNotExist:
            # Gérez le cas où la commande n'existe pas
            print('problem')
            pass
    elif ipn_obj.payment_status == "Pending":
        print('problem')

        
    else:
        # Transactions annulées ou refusées
        ...
        print('echec')


