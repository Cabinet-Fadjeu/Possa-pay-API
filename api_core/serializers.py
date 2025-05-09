from rest_framework import serializers

class URLParamsSerializer(serializers.Serializer):
    productName = serializers.CharField(required=True)
    amnt = serializers.CharField(required=True)
    currency = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    serviceKey = serializers.CharField(required=True)
    payType = serializers.CharField(required=True)
    productId = serializers.CharField(required=True)