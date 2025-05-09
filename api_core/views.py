from django.shortcuts import render
from django.urls import reverse
import decimal
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from rest_framework.decorators import api_view, permission_classes
from userAuth.models import CustomUser, Wallet, Compte, Service
from .serializers import URLParamsSerializer
from django.http import JsonResponse
from django.shortcuts import redirect
import stripe
from .models import apiCoreTransactions


stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
# @api_view(['POST'])
def api_core_view (request):
    serializer = URLParamsSerializer(data=request.GET,)
    if serializer.is_valid():
        data = serializer.validated_data
        print(f'validated data are : {data}')
        try :
            user = CustomUser.objects.get(email = data['email'])
            service = Service.objects.get(public_key = data['serviceKey'])
            if service.user == user : 
                payData = {
                    'amount' : data['amnt'],
                    'currency' : data['currency'],
                    'productName' : data['productName'],
                    'payType' : str(data['payType']).capitalize()
                }
                transaction = apiCoreTransactions.objects.create(
                    user = user,
                    service = service,
                    amount = decimal.Decimal(data['amnt']),
                    currency = str(data['currency']).upper(),
                    payment_type = str(data['payType']).upper(),
                    productId = data['productId'],
                    productName = str(data['productName']).capitalize(),
                    transaction_status = 'PENDING'
                )
# For Paypal template
                if str(data['payType']).lower() == 'paypal':
                    # Load Paypal instance
                    host = request.get_host()
                    paypal_dict = paypal_payment(host, transaction.id, data['amnt'], data['productName'], data['currency'])
                    return render(request, 'home_core.html', {'paypal_data': paypal_dict, 'payData'  : payData })
            
# For Stripe Payment template
                if str(data['payType']).lower() == 'card':
                    context = stripe_payment(data['amnt'],data['currency'])
            
                    return render(request, 'stripe_template.html', {'context' : context, 'payData'  : payData })
            
# For Possa Pay template
                if str(data['payType']).lower() == 'possapay':

                    return render(request, ' possapay_template.html', {'context' : context, 'payData'  : payData })
                
# For Mobile template  
                if str(data['payType']).lower() == 'mobile':
                    pass
            return JsonResponse('User not authorized', safe=False, status=401)
        except Exception as e:
            return JsonResponse('User or service not found', safe=False, status=400)

    return JsonResponse({'error': serializer.errors}, status=400)



    # paypal_dict = {
    #     'business': settings.PAYPAL_RECEIVER_EMAIL,
    #     'amount': str(20),  
    #     'item_name': 'Recharge Wallet',
    #     'invoice': 'INV-{}'.format(4658),
    #     'currency_code': "EUR",
    #     'notify_url': 'http://{}{}'.format(host, reverse("core:paypal-ipn")),
    #     'return_url': 'http://{}{}'.format(host, reverse("core:pending_page")),
    #     'cancel_url': 'http://{}{}'.format(host, reverse("core:cancel")),

    # }

    # paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)


    # return render(request, 'home_core.html', {'paypal_payment_button': paypal_payment_button,})


def paypal_payment (host, transaction_id, price, productName,currency):
    paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': str(price),
            'item_name':  str(productName).capitalize,
            # 'invoice': 'INV-{}'.format(4658),
            'invoice' : transaction_id,
            'currency': str(currency).upper,
            'notify_url': 'http://{}{}'.format(host, reverse("core:paypal-ipn")),
            'return_url': 'http://{}{}'.format(host, reverse("core:pending_page")),
            'cancel_url': 'http://{}{}'.format(host, reverse("core:cancel")),
        }
    return paypal_dict

def stripe_payment(price, currency):
    try:
       
        amount = int(float(price) * 100)
        currency = str(currency).lower()

        # Create PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            metadata={'integration_check': 'accept_a_payment'},
        )

        return {
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'client_secret': intent.client_secret,
        }

    except Exception as e:
        # Optional: handle or log the error
        print(f"Stripe error: {e}")
        return {
            'error': str(e)
        }
    # session = stripe.checkout.Session.create(
    #         payment_method_types=['card'],
    #         line_items=[{
    #             'price_data': {
    #                 'currency': str(currency).lower(),
    #                 'product_data': {
    #                     'name': str(productName).capitalize(),
    #                 },
    #                 'unit_amount': price, 
    #             },
    #             'quantity': 1,
    #         }],
    #         mode='payment',
    #         success_url= reverse("core:pending_page"),
    #         cancel_url= reverse("core:cancel"),
    # )
def possapay_payment(request):
    pass

def mobile_payment(request):
    pass


@api_view(['PUT'])
def modify (request, transacationID):
    try :
        pass
    except Exception:
        pass


