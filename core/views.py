from django.http import JsonResponse
from decimal import Decimal
import math
from django.http import Http404,HttpResponse
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import redirect,render,get_object_or_404

# from rest_framework.decorators import api_view,permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from userAuth.models import CustomUser,Wallet
from .utils import send_order_notification


from django.contrib.auth.hashers import check_password

from .models import Transfer, RechargeWallet,Retreat,Transaction
# from .serializer import (
#     RechargeWalletSerializer, TransferSerializer, RetreatSerializer
# )
import stripe
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received



#home
def index(request):
    return render(request, 'core/index.html')

#profile
def profile_view(request):
    
    return render(request, 'core/profile.html')


@login_required 
def makeTransfer(request):
    user = request.user
    sender_country = user.country
     # Vérifier le portefeuille de l'expéditeur et recuperer la devise
    
    try:
        sender_wallet = Wallet.objects.get(user_id=user.id)
        devise = sender_wallet.devise
    except Wallet.DoesNotExist:
        messages.error(request, "Vous n'avez pas de portefeuille associé.")
        return redirect('core:make_transfer')
    
    #1er requete envoie d'argent
    if request.method == 'POST':
        email = request.POST.get("recipient_email")
        phone = request.POST.get("phone")
        amount_1 = request.POST.get("montant")
        receiver_type = request.POST.get("receiver_type")

        statut = 'lock' if receiver_type  == 'entreprise' else 'Pending'

        # Vérification des champs obligatoires
        if not all([email, amount_1, devise, receiver_type,]):
            # print('email:',email, amount_1, devise, receiver_type, )
            messages.warning(request, "Tous les champs sont requis.")
            return redirect("core:make_transfer")

        try:
            amount_1 = Decimal(amount_1)
            if amount_1 <= 0:
                raise ValueError("Le montant doit être positif.")
        except (ValueError, TypeError):
            messages.warning(request, "Montant invalide.")
            return redirect("core:make_transfer")
            
        try:
            receiver = CustomUser.objects.get(email=email)
            receiver_country = receiver.country
            receiver_wallet = Wallet.objects.get(
                    user_id=receiver.id,
                )
            to_devise = receiver_wallet.devise

        except CustomUser.DoesNotExist:
            messages.warning(request, f"Il n'existe aucun utilisateur avec l'email : {email}")
            return redirect("core:make_transfer")
            
         # Calcul des frais d'assurance et frais d'envois
        amount_assur = (2 * amount_1) / 100 if receiver_type == "entreprise" else 0
        frais = 0 if sender_country  == receiver_country else (2 * amount_1) / 100
        if devise == 'XAF':
            frais = math.ceil(frais)
            amount_assur = math.ceil(amount_assur)
        elif devise == 'EUR':
            frais = round(frais, 2)
            amount_assur = round(amount_assur,2)
            
        total_amount = amount_1 + amount_assur + frais
        

        if devise == to_devise:
            receiver_amount=amount_1
        elif devise == 'XAF' and to_devise == 'EUR':
            receiver_amount=amount_1 / 655.957
        elif devise == 'EUR' and to_devise == 'XAF':
            receiver_amount=amount_1 * 655.957
        else:
            # Si aucune des conditions ci-dessus n'est remplie, lever une exception
            raise ValueError(f"La conversion entre {devise} et {to_devise} n'est pas définie.")

       

        # Vérifier le mot de passe secret
        # if not check_password(secret_code, user.secret_code):
        #         messages.warning(request, "Mot de passe incorrect.")
        #         return redirect("core:make_transfer")

        # Vérifier le solde disponible
        if sender_wallet.amount < total_amount:
                print('sender_wallet.amount:',sender_wallet.amount,'total_amount', total_amount)

                messages.warning(request, "Vous n'avez pas assez d'argent dans votre compte.")
                return redirect("core:make_transfer")

        request.session['transaction_data'] = {
                'receiver_email': email,
                'receiver_name': receiver.get_full_name(),
                'receiver_phone': receiver.phone_number,
                'amount_1': float(amount_1),
                'receiver_amount': float(receiver_amount),
                'total_amount': float(total_amount),
                'currency': devise,
                'to_devise': to_devise,
                'sender_country':sender_country,
                'receiver_country':receiver_country,
                'receiver_type': receiver_type,
                'amount_assur': float(amount_assur),
                'frais': float(frais),
                'statut':statut
            }
        return redirect("core:confirm-transaction")  
    

    context = {
        "devise": devise,
    }
    return render(request, 'core/transfert.html',context)

#confirme transaction
@login_required
def confirmTransaction(request):
    transaction_data = request.session.get('transaction_data')
    print('transaction_data:',transaction_data)

    if not transaction_data:
            messages.error(request, "Aucune transaction à confirmer.")
            return redirect('core:make_transfer')
    if request.method == 'POST':
        print('transaction_data:',transaction_data)
        user = request.user
        receiver_email = transaction_data['receiver_email']
        receiver_name = transaction_data['receiver_name']
        receiver_phone = transaction_data['receiver_phone']
        amount = Decimal(transaction_data['amount_1'])
        receiver_amount = transaction_data['receiver_amount']
        devise = transaction_data['currency']
        frais = transaction_data['frais']
        total_amount = Decimal(transaction_data['total_amount'])
        receiver_type = transaction_data['receiver_type']
        statut = transaction_data['statut']
        from_country = transaction_data['sender_country']
        to_country = transaction_data['receiver_country']
        amount_assur = transaction_data['amount_assur']
        to_devise = transaction_data['to_devise']
        secret_code = request.POST.get("password")   

        # print('transaction_data:',receiver_email,receiver_type,amount)
        

        if not transaction_data:
            messages.error(request, "Aucune transaction à confirmer.")
            return redirect('core:make_transfer')

        # from_country=user.country      
        statut = transaction_data['statut']
        from_country = transaction_data['receiver_country']
        amount_assur = Decimal(transaction_data['amount_assur'])

        # Vérifier le mot de passe secret
        if not check_password(secret_code, user.secret_code):
                messages.warning(request, "Mot de passe incorrect.")
                return redirect("core:make_transfer")
        
        try:
            receiver = CustomUser.objects.get(email=receiver_email)
            to_country = receiver.country
            receiver_wallet = Wallet.objects.get(
                    user_id=receiver.id,
                )
            to_devise = receiver_wallet.devise
        except CustomUser.DoesNotExist:
            messages.error(request, "Le récepteur n'existe plus.")
            return redirect('core:make_transfer')


        try:
            with transaction.atomic():
                # Vérifier si le récepteur existe
               
                sender_wallet = Wallet.objects.get(user_id=user.id)
                
                # Vérifier le solde de l'expéditeur
                if sender_wallet.amount < total_amount:
                    messages.error(request, "Fonds insuffisants.")
                    return redirect('core:make_transfer')
            
                
                # Compte frais
                
                fees_wallet =Wallet.objects.get(user_id='ce67d2d02dcc407fa049e025be9205fa')
                print('hello',fees_wallet)
                # Effectuer la transaction
                sender_wallet.amount -= total_amount
                sender_wallet.save()

                if frais>0:
                    fees_wallet.amount += Decimal(frais)
                    fees_wallet.save()

                if amount_assur>0:
                    fees_wallet.amount += Decimal(amount_assur)
                    fees_wallet.save()

                if statut == 'lock':
                    fees_wallet.amount += Decimal(receiver_amount)
                    fees_wallet.save()
                else:
                    receiver_wallet.amount += Decimal(receiver_amount)
                    receiver_wallet.save()

                statut = 'completed' if statut == 'pending' else statut

                # Enregistrer la transaction
                Transaction.objects.create(
                    sender=user,
                    receiver=receiver,
                    amount=amount,
                    currency=devise,
                    receiver_type=receiver_type,
                    payment_mode='PossaPay', 
                    amount_assur=amount_assur,
                    from_country=from_country,
                    to_country=to_country,
                    status= statut,
                    frais=frais,
                    transaction_type='Envoi',
                    receiver_amount=receiver_amount,
                    receiver_currency=to_devise,
                )

                # Supprimer les données de la session
                del request.session['transaction_data']

                messages.success(request, "Transaction effectuée avec succès.")
                return redirect('core:index')

        except Exception as e:
            messages.error(request, f"Une erreur s'est produite : {str(e)}")
            return redirect('core:make_transfer')


    # Si GET, afficher le formulaire de transfert
    
    
    return render(request, 'core/confirm.html',{"transaction": transaction_data})

@login_required
def solde(request):
    user=request.user
    transactions = Transaction.objects.filter(sender=user).select_related('receiver')
    sender_wallet = Wallet.objects.get(user_id=user.id)
    amount =sender_wallet.amount
    devise =sender_wallet.devise
    transactions = Transaction.objects.filter(sender=user)
    
    context ={
        "amount":amount,
        "devise":devise,
        "transactions":transactions
    }

    return render(request, 'core/solde.html', context)

@login_required
def modifier_statut(request,transaction_id):
    user=request.user
    transactionn = get_object_or_404(Transaction, id=transaction_id)
    if transactionn.sender != user:
        messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page.")
        return redirect('core:solde')
    if transactionn.status != 'lock':
        messages.error(request, "Vous ne pouvez pas modifier le statut de cette transaction.")
        return redirect('core:index')
    if request.method == 'POST':
            recceiver = transactionn.receiver
            amount = transactionn.amount
            receiver_wallet = Wallet.objects.get(user_id=recceiver.id)
            with transaction.atomic():
                receiver_wallet.amount += amount
                receiver_wallet.save()
                transactionn.status='completed'
                transactionn.save()
                messages.success(request, "Statut de la transaction modifié avec succès.")
                return redirect('core:solde')
            
    
    
    return render(request, 'core/statut_modifier.html', 
                #   {'transaction': transaction}
                  )

@login_required
def recharge_wallet(request):
    user = request.user
    
     # Vérifier le portefeuille de l'expéditeur
    try:
        user_wallet = Wallet.objects.get(user_id=user.id)
    except Wallet.DoesNotExist:
        messages.error(request, "Vous n'avez pas de portefeuille associé.")
        return redirect('core:index')
    # devise = user_wallet.devise.lower()
    devise = user_wallet.devise

    if request.method == 'POST':
        amount = request.POST['montant']
        mode = request.POST['payment_mode']
        if mode == 'Visa':
            mode = 'CARTE_CREDIT'
        if amount.isdigit():
            amount = Decimal(amount)
            if amount <= 0:
                messages.error(request, "Le montant doit être positif.")
                return redirect('core:Recharge')
        else:
            messages.error(request, "Montant invalide.")
            return redirect('core:Recharge')
        # total_amount = amount

        #recharge wallet
        transaction =Transaction.objects.create(
            sender=user,
            amount=amount,
            currency=devise,
            payment_mode=mode, 
            status= 'pending',
            transaction_type='Recharge',
        )
        print('mode:',mode)
        print('transaction1:',transaction)
        print('mode1:',transaction.payment_mode)
        
        if devise == 'XAF':
            total_amount=amount/655
        elif devise =='EURO':
            total_amount = amount
        else:
            messages.error(request, " devise non prise en compte")
            return redirect('core:index')

        if mode =="PayPal":
            print('paypal')
            return render_checkout_page_paypal(request, total_amount,transaction)
        elif mode =="CARTE_CREDIT":
            print('CARTE_CREDIT')
            return render_checkout_page_stripe(request, total_amount,transaction)
        else:
            messages.error(request, "il faut choisire un mode de payment")
            return redirect('core:index')
        
    context = {
        "devise": devise,
    }

    return render(request, 'core/recharge.html',context)

# def render_checkout_page_stripe(request, amount):
#     """
#     Rend la page de paiement avec les détails de la commande.
#     """
#     try:
#         stripe.api_key = settings.STRIPE_SECRET_KEY

#         total_amount_in_cents = int(amount * 100)
#         # Créer une session de paiement Stripe avec le montant dynamique
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=["card"],  # Ajouter d'autres modes si nécessaire
#             line_items=[
#                 {
#                     "price_data": {
#                         "currency": "eur",
#                         "product_data": {
#                             "name": "Recharge de portefeuille",  # Nom affiché dans le checkout Stripe
#                         },
#                         "unit_amount": total_amount_in_cents,  # Montant dynamique
#                     },
#                     "quantity": 1,
#                     "metadata":{
#                     # 'order_id': str(order.id),
#                     # 'order_sku': order.sku
#         },
#                 }
#             ],
#             mode="payment",
#             success_url=request.build_absolute_uri(reverse("core:success")),
#             cancel_url=request.build_absolute_uri(reverse("core:cancel")),
#         )
#         return redirect(checkout_session.url, code=303)
#     except Exception as e:
#         messages.error(request, f"Une erreur est survenue : {str(e)}")
#         return redirect('core:Recharge')

def render_checkout_page_stripe(request, amount,transaction):

    stripe.api_key = settings.STRIPE_SECRET_KEY
    total_amount_in_cents = int(amount * 100)

    try:
        checkout_session = stripe.checkout.Session.create(
    payment_method_types=["card"],
    line_items=[{
        "price_data": {
            "currency": "eur",
            "product_data": {
                "name": "Recharge de portefeuille",
            },
            "unit_amount": total_amount_in_cents,
        },
        "quantity": 1,
    }],
    mode="payment",
    success_url=request.build_absolute_uri(reverse("core:pending_page")) + "?session_id={CHECKOUT_SESSION_ID}",
    cancel_url=request.build_absolute_uri(reverse("core:cancel")),
    
    # ✅ Ajout des métadonnées au PaymentIntent
    payment_intent_data={
        "metadata": {
            "transac_id": str(transaction.id)
        }
    }
)

        transaction = Transaction.objects.filter(sender=request.user, status='Pending', id=transaction.id).first()
        print('transaction2:', transaction)
        if transaction:  # Vérifie si un objet a été trouvé
            transaction.session_id = checkout_session.id
            transaction.save()
        else:
            print("⚠️ Aucune transaction trouvée avec ces critères.")

        return redirect(checkout_session.url, code=303)

    except Exception as e:
        from django.contrib import messages
        messages.error(request, f"Une erreur est survenue : {str(e)}")
        return redirect('core:Recharge')



def success(request):
    return render(request, "core/success.html")


def cancel(request):
    return render(request, "core/cancel.html")


def pending_page(request):
    return render(request, "core/pending.html")

#paypal


def render_checkout_page_paypal(request,amount,transaction):
    paypal=settings.PAYPAL_RECEIVER_EMAIL
    print('paypal:',paypal)
    """
    Rend la page de paiement avec les détails de la commande.
    """

    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(amount),  # Assure-toi que c'est une string
        'item_name': 'Recharge Wallet',
        'invoice': 'INV-{}'.format(transaction.id),
        'currency_code': "EUR",
        'notify_url': 'http://{}{}'.format(host, reverse("core:paypal-ipn")),
        'return_url': 'http://{}{}'.format(host, reverse("core:pending_page")),
        'cancel_url': 'http://{}{}'.format(host, reverse("core:cancel")),

    }

    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)


    return render(request, "core/checkout.html", {
        
        'paypal_payment_button': paypal_payment_button,
        
    })




#payment complet
def payment_completed_view(request):
    return render(request, "core/payment-completed.html")

#payment failed
def payment_failed_view(request):
    return render(request, "core/payment-failed.html")


@csrf_exempt
def stripe_webhook(request):
    import stripe
    from django.http import JsonResponse
    from django.conf import settings

    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.WEBHOOK  # Remplace avec ton secret Webhook

    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")

    if not sig_header:
        return JsonResponse({'error': 'Stripe-Signature header missing'}, status=400)

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # Log de l’événement reçu
    print("🔔 Événement Stripe reçu :", event['type'])
    print("🔔 contenu :", event)

    if event['type'] == 'payment_intent.succeeded':
        transac_id = event['data']['object']['metadata']['transac_id']
        
        print(f"num : {transac_id}")

        try:
            recharge = Transaction.objects.get(id=transac_id)
            print(f"✅ Transaction trouve ! Transaction {recharge} .")
            recharge.status = 'Completed'
            recharge.save()

            #ccrediter le wallet
            amount =recharge.amount
            user=recharge.sender
            sender_wallet = Wallet.objects.get(user_id=user.id)
            sender_wallet.amount += Decimal(amount)
            sender_wallet.save()


            print(f"✅ Paiement validé ! Transaction {transac_id} mise à jour.")
        except Transaction.DoesNotExist:
            print(f"⚠️ Transaction {transac_id} introuvable.")

        except Exception as e:
            print(f"⚠️ Une erreur s'est produite : {str(e)}")
            
            
    return JsonResponse({'status': 'success'}, status=200)

def check_payment_status(request):
    session_id = request.GET.get("session_id")
    
    if not session_id:
        return JsonResponse({"error": "Session ID is required"}, status=400)

    
    try:
        transaction = Transaction.objects.get(session_id=session_id)
        print('transaction',transaction.status)
        return JsonResponse({"status": transaction.status})
    except Transaction.DoesNotExist:
        print('vide')
        return JsonResponse({"status": "not_found"})


@receiver(valid_ipn_received)
def paypal_ipn_handler(sender, **kwargs):
    ipn = sender

    # Vérifier que le paiement a été réussi
    if ipn.payment_status == "Completed":
        # Récupérer les informations du paiement
        print('reussi paypal 1')
        print('ipn',ipn)

        try:
            transac_id = ipn.invoice.replace("INV-", "")
            recharge = Transaction.objects.get(id=transac_id)
            print(f"✅ Transaction trouve ! Transaction {recharge} .")
            recharge.status = 'Completed'
            recharge.save()

            #ccrediter le wallet
            amount =recharge.amount
            user=recharge.sender
            sender_wallet = Wallet.objects.get(user_id=user.id)
            sender_wallet.amount += Decimal(amount)
            sender_wallet.save()


            print(f"✅ Paiement validé ! Transaction {transac_id} mise à jour.")
        except Transaction.DoesNotExist:
            print(f"⚠️ Transaction {transac_id} introuvable.")
    
    return HttpResponse("Payment not completed", status=400)



