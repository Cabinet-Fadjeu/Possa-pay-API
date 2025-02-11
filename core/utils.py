# utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_order_notification(order, products):
    subject = f'Nouvelle commande #{order.id}'
    product_details = "\n".join([f"Produit : {product.item} - Quantité : {product.qty}" for product in products])
    message = f"""
    Bonjour,

    Nous sommes ravis de vous informer que vous avez reçu une nouvelle commande d'un montant de {order.price}€. Voici les détails de la commande :

    {product_details}

    

    Cordialement,
    Equipe Remethesauce
    """
    recipient_list = ['cabinetfadjeu@gmail.com']
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

