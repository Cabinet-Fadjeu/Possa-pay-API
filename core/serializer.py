from rest_framework import serializers


from .models import Transfer,RechargeWallet, Retreat
from userAuth.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','phone_number']

class RetreatSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Retreat
        fields = ['id','user','amount','currency', 'retreat_type','retreat_info', 'state', 'issuer','request_date', 'issued_date',]


class TransferSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transfer
        fields = ['sender_email','amount','receiver_email','transfer_date','message']
       

class RechargeWalletSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RechargeWallet
        fields = ['account_email','amount','recharge_method','recharge_date','recharge_status','sender_email']
       