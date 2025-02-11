from paypal.standard.models import ST_PP_COMPLETED
from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received
# from .models import CartOrder, CartOrderProducts
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
        # try:
        #     
        # except CartOrder.DoesNotExist:
        #     # Gérez le cas où la commande n'existe pas
        #     print('problem')
        #     pass
    elif ipn_obj.payment_status == "Pending":
        print('problem')

        
    else:
        # Transactions annulées ou refusées
        ...
        print('echec')


