# from django.http import JsonResponse
# from django.shortcuts import render

import re
# from rest_framework.decorators import api_view,permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from rest_framework import generics
import random
import uuid
# from django_cryptography.fields import encrypt

# from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, UntypedToken

from django.contrib.auth.hashers import make_password,check_password
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from .models import CustomUser,Wallet,Service, Compte
# from .serializer import (
#     RegisterSerializer, 
#     UserSerializer, 
#     ChangePasswordSerializer, PhoneNumberSerializer,
#     UserWalletSerializer, UserSecretSerializer
# )
from django.shortcuts import redirect, render
from userAuth.forms import UserRegisterForm
from .forms import CodeSecretForm 
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



# Set or update user Secret code
@login_required
def set_secret_code(request):
    user=request.user

    if request.method == 'POST':
        form = CodeSecretForm(request.POST)
        if form.is_valid():
            # Traitez les données du formulaire ici 
            code_secret = form.cleaned_data['code_secret']
            print(code_secret)
            # Faites quelque chose avec le code secret
            if not user.secret_code_status :
                user.secret_code = make_password(code_secret)
                user.secret_code_status = True
                user.save()
                messages.success(request, 'Code secret enregistré avec succès')
                return redirect('core:index')
            else:
                messages.warning(request, 'Le code secret existe déjà')
                return redirect('core:index')
        else:
            print(form.errors)
    else:
        form = CodeSecretForm()


    context = {
        'form': form,
    }
    return render(request, 'userAuth/passwordWallet.html', context)



# def set_user_secret(request,request_type,user_id):
#     try : 
#         user =  CustomUser.objects.get(id = user_id)
#         if request_type == "set_secret_code" :
#             secret_regex = "^\+?1?\d{5}$"
#             # obj = {'secret_code' : request.data['secret_code']}
#             # serializer = UserSecretSerializer(data = obj, many = False)
#             if not re.match(secret_regex, request.data['secret_code']):
#                 return Response({"msg":"Error : Incorrect secret format!"}, status.HTTP_400_BAD_REQUEST)
#             # if serializer.is_valid():
#             if not user.secret_code_status :
#                 user.secret_code = make_password(request.data['secret_code'])
#                 user.secret_code_status = True
#                 user.save()
#                 return Response({"msg":"success : secret code set"})
#             return Response({"msg":"Error : Secret already exist"},status.HTTP_400_BAD_REQUEST)
#             # return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            
        
#         elif request_type == "change_secret_code" :
#             if user.secret_code_status:
#                 if check_password(request.data['old_secret_code'], user.secret_code) : 
#                     user.secret_code = make_password(request.data['new_secret_code'])
#                     user.save()
#                     return Response({"msg":"success : secret code changed "})
#                 return Response({"msg" : "Error : Secret code unmatched"}, status.HTTP_400_BAD_REQUEST)
#             return Response({'msg' : 'Error : No secret for current user'}, status.HTTP_400_BAD_REQUEST)
        
#         elif request_type == "reset_secret_code" :
#             pass
        
#     except ObjectDoesNotExist:
#         raise Http404

#Check SecretCode Match
# @api_view(["POST"])
# def check_secret_code(request):
#     userId = request.data['id']
#     user_secret = request.data['secret_code']
    
#     user = CustomUser.objects.get(id=userId)
   
#     if check_password(user_secret, user.secret_code):
#         return Response({'status' : True})
#     return Response({'status' : False})


# Get user wallet
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_wallet(request,user_id):
#     wallet = Wallet.objects.get(user_id = user_id)
#     serializer = UserWalletSerializer(wallet, many = False)
#     # response = encrypt_message(serializer.data)
#     return Response(serializer.data, status.HTTP_200_OK)



# Register user
@csrf_exempt
def register_view(request):
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            # Ajouter le pays depuis le champ caché
            new_user.country = form.cleaned_data['country']
            new_user.save()
            new_user = form.save()
            
            messages.success(request," Votre compte a été créé avec succès.")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    phone_number=form.cleaned_data['phone_number'],
                                    password=form.cleaned_data['password1']
            )
            login(request, new_user)
            # user = CustomUser.objects.get(email = obj['email'])
            Wallet.objects.create(user_id = new_user)
            return redirect("userAuth:set-secret")
            
    else:
        form = UserRegisterForm()


    context = {
        'form': form,
    }
    return render(request, "userAuth/sign-up.html", context)

#login
@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Vous ets connecté en tant que : {request.user}")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email") # peanuts@gmail.com
        password = request.POST.get("password") # getmepeanuts

        try:
            user = CustomUser.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user) 
                return redirect("core:index")
            else:
                messages.warning(request, "mot de pass incorrect.")
    
        except:
            messages.warning(request, f"Il n'existe aucun utilisateur avec l'email: {email}")

    return render(request, "userAuth/sign-in.html")

#logout
def logout_view(request):
    logout(request)
    messages.success(request, "You logged out.")
    return redirect("core:index")

#page api
@login_required
def service_dashboard(request):
    user= request.user
    # user.is_company = False
    # user.save()
    # print('statut',user.is_company)
    
    if not user:
        messages.success(request, "un probleme es survenu.")
        return redirect("core:index")
    
    
    if not user.is_company == True:
        messages.success(request, "Vous n'etes pas une entreprise.")
        return redirect("userAuth:service_demand")
    
    service= Service.objects.filter(user=user)
    print('service',service)
    context = {
        'service': service,
    }

    
    return render(request, "userAuth/service_dashboard.html", context)


#service demande
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
@login_required
def service_demand(request):
    user=request.user
    if not user:
        messages.error(request, "Utilisateur introuvable.")
        return redirect("core:index")
    if user.is_company == True:
        return redirect("userAuth:service_dashboard")
    if request.method =='POST':
        
        user.is_company=True
        user.save()
        
        messages.success(request, "Demande de service envoyée")
        return redirect("userAuth:service_dashboard")

    return render(request, "userAuth/service_demand.html")

#ceer service
@login_required
def create_service(request):
    user = request.user
    if not user:
        messages.error(request, "Utilisateur introuvable.")
        return redirect("core:index")
    if user.is_company == False:
        return redirect("userAuth:service_demand")
    if request.method == 'POST':
        #creer le service
        try:
            # Récupérer les données envoyées par la requête
            name = request.data.get("name")  # Nom du service
            description = request.data.get("description", "")  # Description facultative
            allowed_hosts = request.data.get("allowed_hosts", "")  # Hôtes autorisés facultatifs

            # Utiliser une transaction pour s'assurer que tout est créé ensemble
            with transaction.atomic():
            # Créer un compte
                compte = Compte.objects.create(
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

        #service = Service.objects.create(user=user, name=name, description=description, compte=compte, allowed_hosts=allowed_hosts)
            messages.success(request, "Service créé avec succès.")
            return redirect("userAuth:service_dashboard")
        
        except Exception as e:
            messages.success(request, "probleme est survenu.",e)
            return redirect("userAuth:service_dashboard")
    
    return render(request, "userAuth/create_service.html")

# delete service
@login_required
def delete_service(request, service_id):
    user = request.user
    if not user:
        messages.error(request, "Utilisateur introuvable.")
        return redirect("core:index")
    if user.is_company == False:
        return redirect("userAuth:service_demand")
    service = Service.objects.get(user=user, id=service_id)
    service.delete()
    messages.success(request, "Service supprimé avec succès.")
    return redirect("userAuth:service_demand")

#pdater service
@login_required
def update_service(request, service_id):
    user = request.user
    if not user:
        messages.error(request, "Utilisateur introuvable.")
        return redirect("core:index")
    if user.is_company == False:
        return redirect("userAuth:service_demand")
    service = Service.objects.get(user=user, id=service_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        allowed_hosts = request.POST.get('allowed_hosts')
        service.name = name
        service.description = description
        service.allowed_hosts = allowed_hosts
        service.save()
        messages.success(request, "Service mis à jour avec succès.")
        return redirect("userAuth:service_dashboard")
    return render(request, "userAuth/update_service.html")

# @api_view(['POST'])
# def create_service(request, user_id):
#     origin = request.META.get('HTTP_ORIGIN')
#     print('origine:',origin)
#     try:
#         user = CustomUser.objects.get(id=user_id)

#         # Récupérer les données envoyées par la requête
#         name = request.data.get("name")  # Nom du service
#         description = request.data.get("description", "")  # Description facultative
#         allowed_hosts = request.data.get("allowed_hosts", "")  # Hôtes autorisés facultatifs

#         # Utiliser une transaction pour s'assurer que tout est créé ensemble
#         with transaction.atomic():
#             # Créer un compte
#             compte = Compte.objects.create(
#                 amount=0.00  # Valeur par défaut
#             )

#             # Créer un service et lier le compte
#             service = Service.objects.create(
#                 user=user,
#                 name=name,
#                 description=description,
#                 compte=compte,
#                 allowed_hosts=allowed_hosts
#             )

#         # Retourner une réponse JSON avec les détails
#         return Response({
#             "message": "Service créé avec succès.",
#             "service_id": service.id,
#             "public_key": service.public_key,
#             "secret_key": service.secret_key,
#             "compte_id": compte.id,
#             "compte_amount": compte.amount,
#         }, status=201)

#     except CustomUser.DoesNotExist:
#         return Response({"error": "Utilisateur introuvable."}, status=404)
#     except Exception as e:
#         return Response({"error": str(e)}, status=500)
