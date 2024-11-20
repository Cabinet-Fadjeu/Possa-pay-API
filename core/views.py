# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from .models import User, Wallet, Transaction

# @login_required
# def send_money(request, receiver_id):
#     receiver = get_object_or_404(User, id=receiver_id)
#     if request.method == 'POST':
#         amount = float(request.POST['amount'])
#         transaction = Transaction(sender=request.user, receiver=receiver, amount=amount)
#         if transaction.process_transaction():
#             return redirect('success_page')  # Redirige vers une page de succès
#         else:
#             return render(request, 'send_money.html', {'error': 'Solde insuffisant'})
#     return render(request, 'send_money.html', {'receiver': receiver})



# -----------gpt---------------------

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Service, Transaction

# @api_view(['POST'])
# def process_payment(request):
#     data = request.data
#     public_key = data.get('public_key')
#     secret_key = data.get('secret_key')
#     amount = data.get('amount')

#     try:
#         # Vérifier le service par ses clés
#         service = Service.objects.get(public_key=public_key, secret_key=secret_key)
#         service_wallet = service.wallet

#         if service_wallet and amount:
#             # Créer la transaction et l’enregistrer
#             transaction = Transaction.objects.create(
#                 sender_wallet=None,  # Le client ou utilisateur anonyme
#                 recipient_wallet=service_wallet,
#                 amount=amount,
#                 transaction_type='service_payment',
#                 status='completed'
#             )
#             return Response({"status": "success", "transaction_id": transaction.id}, status=status.HTTP_200_OK)
#         else:
#             return Response({"status": "error", "message": "Invalid transaction data"}, status=status.HTTP_400_BAD_REQUEST)
    
#     except Service.DoesNotExist:
#         return Response({"status": "error", "message": "Invalid service credentials"}, status=status.HTTP_403_FORBIDDEN)


# ------small possa-------

import decimal
from django.http import Http404

from django.shortcuts import render

from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from userAuth.models import CustomUser,Wallet

from django.contrib.auth.hashers import check_password

from .models import Transfer, RechargeWallet,Retreat
from .serializer import (
    RechargeWalletSerializer, TransferSerializer, RetreatSerializer
)

# Create your views here.

# Making a retreat Request
# @api_view(['POST', 'GET',])
# @permission_classes([IsAuthenticated])
# def requestRetreat(request):
#     if request.method == 'GET':
#         querry = Retreat.objects.all()
#         serialzer = RetreatSerializer(querry, many = True)
#         return Response(serialzer.data)
    
#     elif request.method == 'POST':
#         try : 
#             user =  CustomUser.objects.get(id= request.data['user_id'])
#             userWallet = Wallet.objects.get(user_id = user.id)
#             if user.email_verified == True:
#                 if user.secret_code :
#                     secret_code = request.data['secret_code']
#                     if check_password(secret_code, user.secret_code):
#                         if userWallet.amount >= float(request.data['amount']):
#                             amount_1 = float(request.data['amount'])
#                             wallet_amount = float(userWallet.amount)
#                             result = wallet_amount - amount_1
#                             userWallet.amount = decimal.Decimal(result)
                            
#                             Retreat.objects.create(
#                                 user  = user,
#                                 amount = request.data['amount'],
#                                 currency = request.data['currency'],
#                                 retreat_type = request.data['retreat_type'],
#                                 retreat_info = request.data['retreat_info'],
#                             )
                            
#                             userWallet.save()
#                             return Response("Retreat request success", status.HTTP_200_OK)
#                         return Response({"msg" :"insufficient amount"}, status.HTTP_400_BAD_REQUEST)
#                     return Response({"msg" :"incorrect passcode"}, status.HTTP_400_BAD_REQUEST)
#                 return Response({"msg" :"passcode not set"}, status.HTTP_400_BAD_REQUEST)
#             return Response({"msg" :"Unverified email"}, status.HTTP_400_BAD_REQUEST)
#         except ObjectDoesNotExist :
#             raise Http404

# Making a new recharge
# @api_view(['POST','GET'])
# @permission_classes([IsAuthenticated])
# def makeRecharge(request):
#     if request.method == 'GET':
#         recharge = RechargeWallet.objects.all()
#         serializer = RechargeWalletSerializer(recharge, many = True)
#         return Response(serializer.data)

#     if request.method == 'POST':
        
#         user =  CustomUser.objects.get(email= request.data['account_email'])

       
#         if not user:
#             return Response({"msg" : "Email not found"}, status.HTTP_400_BAD_REQUEST)
       
#         userWallet = Wallet.objects.get(user_id = user.id)

#         userWallet.amount = userWallet.amount + decimal.Decimal(request.data['amount'])

#         recharge = RechargeWallet.objects.create(
#             account_email = user.email,
#             user  = user,
#             amount = request.data['amount'],
#             recharge_method = request.data['recharge_method'],
#             sender_email = request.data['sender_email'],
#             recharge_status = request.data['recharge_status'],
#         )

#         userWallet.save()

#         serializer = RechargeWalletSerializer(recharge, many = False)
#         return Response("Recharge successfull", status.HTTP_200_OK)



# Making a transfer transaction
@api_view(['POST','GET'])
# @permission_classes([IsAuthenticated])
def makeTransfer(request):
    if request.method == 'GET':
        transer = Transfer.objects.all()
        serializer = TransferSerializer(transer, many = True)
        return Response(serializer.data)

    if request.method == 'POST':
        try:
            user =  CustomUser.objects.get(id= request.data['user_id'])
            print('user',user)
            receiver = CustomUser.objects.get(email = request.data['receiver_email'])
            print('receiver',receiver)
            if user.email_verified == True:
                wallet = Wallet.objects.get(user_id = user.id)
                secret_code = request.data['secret_code']
                

                
                if check_password(secret_code, user.secret_code):
                    if wallet.amount >= float(request.data['amount']):
                        #se bloc doit etre dans une transact atomique
                        amount_1 = float(request.data['amount'])
                        wallet_amount = float(wallet.amount)
                        result = wallet_amount - amount_1
                        wallet.amount = decimal.Decimal(result)
                        wallet.save()
                        
                        receiver_wallet =  Wallet.objects.get(user_id = receiver.id)
                            
                        receiver_wallet.amount = receiver_wallet.amount + decimal.Decimal(request.data['amount'])
                        receiver_wallet.save()

                        transfer = Transfer.objects.create(
                            user = user,
                            amount = request.data['amount'],
                            receiver_email  = request.data['receiver_email'],
                            # message = request.data['message']
                        )
                        
                        
                        return Response ({"msg" : "success"})
                    
                    return Response({"msg" :"insufficient amount"}, status.HTTP_400_BAD_REQUEST)
                return Response({"msg" :"incorrect passcode"}, status.HTTP_400_BAD_REQUEST)
            return Response({"msg" : "Unverified email"}, status.HTTP_400_BAD_REQUEST)
        
        except ObjectDoesNotExist:
            raise Http404

    
# # Getting a transaction details
# @api_view(['GET','PUT','DELETE'])
# @permission_classes([IsAuthenticated])
# def getTransfersDetail(request,id):
#     transer = Transfer.objects.get(id=id)

#     if request.method == 'GET':

#         serializer = TransferSerializer(transer, many = False)
#         return Response(serializer.data)

# Getting transfer details
# @api_view(['GET','DELETE'])
# @permission_classes([IsAuthenticated])
# def getTransfersHistory(request,id):
    
#     if request.method == 'GET':
#         try : 
#             user = CustomUser.objects.get(id=id)

#             transers = Transfer.objects.filter(user = user)
            
#             serializer = TransferSerializer(transers, many=True)

#             return Response(serializer.data)
#         except ObjectDoesNotExist : 
#             raise Http404
    
#     if request.methode == 'DELETE':
#         try: 
                
#             tranfer = Transfer.objects.get(id = id)
#             tranfer.delete()

#             return Response("transaction deleted successfully", status.HTTP_200_OK)
        
#         except ObjectDoesNotExist : 
#             return Http404
    

# Getting recharge details
# @api_view(['GET','DELETE'])
# @permission_classes([IsAuthenticated])
# def getRechargeHistory(request,id):
   
#     if request.method == 'GET':
#         try:

#             user = CustomUser.objects.get(id=id)
#             recharge = RechargeWallet.objects.filter(user = user)
#             serializer  = RechargeWalletSerializer(recharge, many=True)
        
#             return Response(serializer.data)
        
#         except ObjectDoesNotExist :
#             raise Http404
    
#     if request.method == 'DELETE':
#         try:
#             recharge =  RechargeWallet.objects.get(id=id)
#             recharge.delete()
#             return Response("Recharge transaction deleted successfully", status.HTTP_200_OK)
        
#         except ObjectDoesNotExist:
#             raise Http404("Recharge transaction not found")
        
        
        


