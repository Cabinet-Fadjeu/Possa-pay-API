from django.http import JsonResponse
from rest_framework.views import APIView
from userAuth.models import AllowedHost,Service
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.shortcuts import redirect,render,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from userAuth.models import CustomUser,Wallet
from core.models import Transaction
#from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from core.convert import convertire



@csrf_exempt
def GeneratePaymentUrl(request):
    if request.method == "POST":
        public_key = request.headers.get('X-API-KEY')
        origin = request.META.get('HTTP_ORIGIN')
        # print('origin2',origin)
        # print('public2',public_key)
        data = request.POST


        if not public_key or not origin:
            return JsonResponse({'error': 'API key or origin missing'}, status=400)

        try:
            service=Service.objects.get(public_key=public_key)
            # print('hello3')
            
        except Service.DoesNotExist:
            # print('danger0')
            return JsonResponse({'error': 'Invalid public key'}, status=403)

        if not AllowedHost.objects.filter(service=service, domain=origin).exists():
            # print('danger1')
            return JsonResponse({'error': 'Origin not allowed'}, status=403)
        try:
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)  # dictionnaire
            # print("Données JSON reçues :", data)

            amount = data.get("amount")
            currency = data.get("currency")
            # notify_url = data.get("notify_url") 
            # return_url = data.get("return_url")
            # cancel_url = data.get("cancel_url")
            # list_url = {
            #     'cancel_url':cancel_url,
            #     'notify_url':notify_url,
            #     'return_url':return_url,
            # }
            # request.session['list_url']= list_url
            # print('hello444',request.session['list_url'])
            

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON invalide'}, status=400)

        #Génération d'un lien de paiement (à adapter selon ton besoin)
        payment_url = f"http://127.0.0.1:8000/externe/api/payment/{public_key}-{amount}-{currency}"
        # payment_url = f"http://127.0.0.1:8000/externe/api/payment/{public_key[:5]}-{data.get('amount', '000')}"
        # print('hello6',payment_url)

    return JsonResponse({'payment_url': payment_url})


def PaymentLogin(request, public_key, amount, devise):
    if request.method == 'POST':
        action = request.POST.get("action")

        if action == "login":
            email = request.POST.get("email")
            password = request.POST.get("password")
            try:
                user = CustomUser.objects.get(email=email)
                user = authenticate(request, email=email, password=password)

                if user is not None:
                    login(request, user)
                    print('connecte')
                    return render(request, 'externe/confirm.html')
                else:
                    messages.warning(request, "Mot de passe incorrect.")
            except CustomUser.DoesNotExist:
                messages.warning(request, f" mot de passe ou email incorrect.")
                return render(request, 'externe/ereur.html')
            # return render(request, 'externe/ereur.html')

        elif action == "confirm":
            # Vérifier si l'utilisateur est connecté
            user = request.user
            if not user.is_authenticated:
                messages.warning(request, "Veuillez vous connecter pour effectuer le paiement.")
                return redirect('core:index')
                
            
            print("Paiement debute")
            
            try:
                with transaction.atomic():
                    amountt = Decimal(amount)  # Convertir le montant en décimal

                        # Vérifier si le montant est valide
                    if amountt <= 0:
                        messages.error(request, "Montant invalide.")
                        return redirect('core:index')
                    
                    # Vérifier si le récepteur existe
                    buyer_wallet = Wallet.objects.get(user_id=user.id)
                    buyer_devise = buyer_wallet.devise
                    print('devise',buyer_devise)

                    
                
                    # Vérifier le solde de l'expéditeur
                    if buyer_wallet.amount < amountt:
                        messages.error(request, "Fonds insuffisants.")
                        return redirect('core:index')
                    
                    if devise != buyer_devise:
                        # Convertir le montant dans la devise du portefeuille de l'utilisateur
                        print('montant debut')
                        try:
                            buyer_amountt = convertire(devise, buyer_devise, amountt)
                        except ValueError as e:
                            messages.error(request, f"Erreur de conversion: {str(e)}")
                            return redirect('core:index')
                    else:
                        buyer_amountt = amountt
                        # print('montant',amountt)

                        # effectuer la transaction
                        #debiter le client
                    buyer_wallet.amount -= buyer_amountt
                    buyer_wallet.save()
                    print('buyer_montant',buyer_wallet.amount)

                    
                    # #crediter le vendeur.
                    service = Service.objects.get(public_key=public_key)
                    receiver = service.user
                    print('service',service)
                    seller_compte = service.compte
                    seller_devise = seller_compte.devise
                    print('devise',seller_devise)

                    if devise != seller_devise:
                        # Convertir le montant dans la devise du portefeuille de l'utilisateur
                        seller_amount = convertire(devise, seller_devise, amountt)
                        print('montant',seller_amount) 
                    else:
                        seller_amount = amountt
                       


                    seller_compte.amount += seller_amount
                    seller_compte.save()
                    
                # Enregistrer la transaction
                # Transaction.objects.create(
                #     sender=user,
                #     receiver=receiver,

                #     amount=amount,
                #     currency=devise,
                #     receiver_type=receiver_type,
                #     payment_mode='PossaPay', 
                #     amount_assur=amount_assur,
                #     from_country=from_country,
                #     to_country=to_country,
                #     status= statut,
                #     frais=frais,
                #     transaction_type='Envoi',
                #     receiver_amount=receiver_amount,
                #     receiver_currency=to_devise,
                # )

                # Supprimer les données de la session
                # del request.session['transaction_data']

                # messages.success(request, "Transaction effectuée avec succès.")
                # return redirect('core:index')

                # 'cancel_url':cancel_url,
                # 'notify_url':notify_url,
                # 'return_url':return_url

                # Rediriger vers l'URL de retour
                # print('return_url')
                # return_ur = request.session['list_url']
                # print('return_url',return_ur)

                # return_url = request.session['list_url']['return_url']
                # print('return_url',return_url)
                
                return render(request, 'externe/success.html', {'amount': amountt, 'devise': devise, 'return_url': return_url})

            except Exception as e:
                messages.error(request, f"Une erreur s'est produitee : {str(e)}")
                return_url = request.session['list_url']['cancel_url']
                return render(request, 'externe/ereur.html', {'amount': amountt, 'devise': devise, 'return_url': return_url})
                
               

            
            

    return render(request, 'externe/sign-in.html')


# def PaymentLogin(request, public_key, amount):
#     if request.method == 'POST':
#         email = request.POST.get("email") # peanuts@gmail.com
#         password = request.POST.get("password") # getmepeanuts

#         try:
#             user = CustomUser.objects.get(email=email)
#             user = authenticate(request, email=email, password=password)

#             if user is not None:
#                 login(request, user)
#                 print('charge10')
#                 if request.method == 'POST':
#                     print('recu20')
#                     # logout(request)
#                     return render(request, 'externe/confirm.html')
#                 return render(request, 'externe/confirm.html')
#                 # return PaymentEnd(request)
            
#             else:
#                 messages.warning(request, "mot de pass incorrect.")
    
#         except:
#             messages.warning(request, f"Il n'existe aucun utilisateur avec l'email: {email}")
#         return redirect('core:index')
#     return render(request, 'externe/sign-in.html')
#     # return render(request, 'payment.html', {'public_key': public_key, 'amount': amount})

# def PaymentEnd (request):
#     if request.method == 'POST':
#         print('recu20')
#         # logout(request)
#         return render(request, 'externe/confirm.html')

#     return render(request, 'externe/confirm.html')

