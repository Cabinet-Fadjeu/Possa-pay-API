# from django.http import JsonResponse
# from django.shortcuts import render

import re
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics
import random
import uuid
# from django_cryptography.fields import encrypt

# from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, UntypedToken

from django.contrib.auth.hashers import make_password,check_password
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from .models import CustomUser,Wallet,Service, Compte
from .serializer import (
    RegisterSerializer, 
    UserSerializer, 
    ChangePasswordSerializer, PhoneNumberSerializer,
    UserWalletSerializer, UserSecretSerializer
)
# from .mixins import MessageHandler,send_email_token
## from utils.encrypt_dec import decrypt_message,encrypt_message

# Create your views here.

# Set or update user Secret code
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def set_user_secret(request,request_type,user_id):
    try : 
        user =  CustomUser.objects.get(id = user_id)
        if request_type == "set_secret_code" :
            secret_regex = "^\+?1?\d{5}$"
            # obj = {'secret_code' : request.data['secret_code']}
            # serializer = UserSecretSerializer(data = obj, many = False)
            if not re.match(secret_regex, request.data['secret_code']):
                return Response({"msg":"Error : Incorrect secret format!"}, status.HTTP_400_BAD_REQUEST)
            # if serializer.is_valid():
            if not user.secret_code_status :
                user.secret_code = make_password(request.data['secret_code'])
                user.secret_code_status = True
                user.save()
                return Response({"msg":"success : secret code set"})
            return Response({"msg":"Error : Secret already exist"},status.HTTP_400_BAD_REQUEST)
            # return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            
        
        elif request_type == "change_secret_code" :
            if user.secret_code_status:
                if check_password(request.data['old_secret_code'], user.secret_code) : 
                    user.secret_code = make_password(request.data['new_secret_code'])
                    user.save()
                    return Response({"msg":"success : secret code changed "})
                return Response({"msg" : "Error : Secret code unmatched"}, status.HTTP_400_BAD_REQUEST)
            return Response({'msg' : 'Error : No secret for current user'}, status.HTTP_400_BAD_REQUEST)
        
        elif request_type == "reset_secret_code" :
            pass
        
    except ObjectDoesNotExist:
        raise Http404

#Check SecretCode Match
@api_view(["POST"])
def check_secret_code(request):
    userId = request.data['id']
    user_secret = request.data['secret_code']
    
    user = CustomUser.objects.get(id=userId)
   
    if check_password(user_secret, user.secret_code):
        return Response({'status' : True})
    return Response({'status' : False})


# Get user wallet
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wallet(request,user_id):
    wallet = Wallet.objects.get(user_id = user_id)
    serializer = UserWalletSerializer(wallet, many = False)
    # response = encrypt_message(serializer.data)
    return Response(serializer.data, status.HTTP_200_OK)



# Register user
@api_view(['POST'])
def register(request):
    
    obj={'username' : request.data['username'], 
         'email' : request.data['email'], 
         'password' : request.data['password']}
    print('obj',obj)

    serializer = RegisterSerializer(data = obj, many = False)

    if serializer.is_valid():
        CustomUser.objects.create_user(
            username = obj['username'],
            email= obj['email'],
            password = obj['password'])
        
        user = CustomUser.objects.get(email = obj['email'])
        Wallet.objects.create(user_id = user)
        return Response( "User and wallet created successfully", status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


#service demande
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def service_demand(request, user_id):
     user =  CustomUser.objects.get(id = user_id)
     user.is_company = True
     user.save()
     print('user',user)
     return Response( "Demand accepted successfully", status.HTTP_201_CREATED)

@api_view(['POST'])
def create_service(request, user_id):
    origin = request.META.get('HTTP_ORIGIN')
    print('origine:',origin)
    try:
        user = CustomUser.objects.get(id=user_id)

        # Récupérer les données envoyées par la requête
        name = request.data.get("name")  # Nom du service
        description = request.data.get("description", "")  # Description facultative
        allowed_hosts = request.data.get("allowed_hosts", "")  # Hôtes autorisés facultatifs

        # Utiliser une transaction pour s'assurer que tout est créé ensemble
        with transaction.atomic():
            # Créer un compte
            compte = Compte.objects.create(
                service_id=user,
                amount=0.00  # Valeur par défaut
            )

            # Créer un service et lier le compte
            service = Service.objects.create(
                user=user,
                name=name,
                description=description,
                compte=compte,
                allowed_hosts=allowed_hosts
            )

        # Retourner une réponse JSON avec les détails
        return Response({
            "message": "Service créé avec succès.",
            "service_id": service.id,
            "public_key": service.public_key,
            "secret_key": service.secret_key,
            "compte_id": compte.id,
            "compte_amount": compte.amount,
        }, status=201)

    except CustomUser.DoesNotExist:
        return Response({"error": "Utilisateur introuvable."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    # return JsonResponse({"error": "Méthode non autorisée."}, status=405)

    # if user.is_company :
    #     Service.objects.create(user = user,
    #                         wallet=user.wallet)
    #     return Response( "successfully", status.HTTP_201_CREATED)



# Set User Profile Image
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def userProfileImageUpdate(request, user_id):
#     try:
#         user = CustomUser.objects.get(id = user_id )

#         if not request.data['profile_img'] :
#             return Response({'msg':'Profile image field empty'}, status = status.HTTP_400_BAD_REQUEST)
        
#         user.profile_img = request.data['profile_img']

#         user.save()

#         return Response("Profile image added successfully")
#     except ObjectDoesNotExist:
#         raise Http404 

# Set user phone number
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def setPhoneNumber(request,id):
#     try :
#         user = CustomUser.objects.get(id = id)
#         obj ={
#             'phone_number' : request.data['phone_number']
#         }
    
#         serializer = PhoneNumberSerializer(data=obj, many=False)

#         if serializer.is_valid():
#             user.phone_OTP = random.randint(10000, 99999)
#             user.phone_number = obj['phone_number']
#             MessageHandler(user.phone_number,user.phone_OTP).send_otp_on_phone()
#             user.save()

#             return Response( "Phone number updated successfully", status.HTTP_200_OK)
        
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
#     except ObjectDoesNotExist:
#         raise Http404
    


# Confirming phone number
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def confirmPhoneNumber(request, id):
#     try : 
#         user = CustomUser.objects.get(id = id)
#         phone_otp = request.data['phone_OTP']

#         if user.phone_OTP == phone_otp :
#             user.phone_verified = True
#             user.save()
#             response = {
#                 "message": "OTP verified"
#             }
#             return Response(response)
#         return Response({'msg':'incorrect Phone OTP'}, status = status.HTTP_400_BAD_REQUEST)
#     except ObjectDoesNotExist:
#         raise Http404


# get, Update, Delete user
# @api_view(['GET','PUT','DELETE'])
# @permission_classes([IsAuthenticated])
# def userDetail(request, id):
#     user = CustomUser.objects.get(id = id)

#     if request.method == 'GET':
#         serializer = UserSerializer(user,context={"request": request}, many = False)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         user.username = request.data['username']
#         #user.email = request.data['email']
#         user.first_name = request.data['first_name']
#         user.last_name = request.data['last_name']
                            
#         # user.secret_code = make_password(request.POST.get('secret_code', None)) #request.data['secret_code']
#         user.profile_img =  request.POST.get('profile_img', None)#request.data['profile_img']
#         user.bio = request.data['bio']

#         user.save()
        
#         access = AccessToken.for_user(user)
#         refresh = RefreshToken.for_user(user)
#         response = {
#             'message':'profile updated',
#             'access' : str(access),
#             'refresh' : str(refresh)
#         }
#         return Response (
#             response
#         )

#     if request.method == 'DELETE':
#         user.delete()

# Changing user email
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def changeEmail(request, id):
#     user = CustomUser.objects.get(id = id)

#     user.email = request.data['email']
    
#     user.email_OTP = None
#     user.email_verified = False
#     user.save()
#     return Response (
#         "Email updated",
#         status.HTTP_200_OK
#     )

# # for changing the password
# class ChangePasswordView(generics.UpdateAPIView):
#     serializer_class = ChangePasswordSerializer
#     model = CustomUser
#     permission_classes = [IsAuthenticated]

#     def get_object(self, id):
#         try:
#             return CustomUser.objects.get(id = id)
#         except CustomUser.DoesNotExist:
#             raise Http404
    
#     def update(self, request, id):
#         self.object = self.get_object(id)
#         serializer = self.get_serializer(data = request.data)

#         if serializer.is_valid():
#             # checking old password
#             if not self.object.check_password(serializer.data.get('old_password')):
#                 return Response({'old_password': 'wrong password'}, status = status.HTTP_400_BAD_REQUEST)
            
#             # Hashing new password user enters
#             self.object.set_password(serializer.data.get('new_password'))
#             self.object.save()
#             response = {
#                 "status" : "succes",
#                 "code" : status.HTTP_200_OK,
#                 "message" : "Password changed successfully",
#                 # "data" : []
#             }
#             return Response(response)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Verifying email address
# @api_view(['PUT', 'GET'])
# @permission_classes([IsAuthenticated])
# def verifyEmail(request, id):

#     user = CustomUser.objects.get(id = id)

#     if request.method == 'GET':
#         user.email_OTP = random.randint(1000000, 9999999)
#         send_email_token(user.email, user.email_OTP)
#         user.save()
#         return Response (
#             {
#                 "status" : "succes",
#                 "code" : status.HTTP_200_OK,
#                 "message" : "Email sent successfully",
               
#             }
#         )
    
#     if request.method == 'PUT':
#         otp = request.data['email_OTP']
#         if user.email_OTP == otp:
#             user.email_verified = True
#             user.save()
#             response = {
#                 "status" : "succes",
#                 "code" : status.HTTP_200_OK,
#                 "message" : "Email verified successfully",
                
#             }
#             return Response(response)
        
#         return Response('Unmatched OTP', status.HTTP_400_BAD_REQUEST)