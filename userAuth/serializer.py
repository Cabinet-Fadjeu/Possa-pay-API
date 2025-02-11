# # from rest_framework.serializers import ModelSerializer

# from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework.validators import UniqueValidator

# from .models import CustomUser, Wallet
# import re
# # from django_cryptography.fields import encrypt





# # Serializer for user wallet
# class UserWalletSerializer(serializers.ModelSerializer):
#     userId = serializers.SerializerMethodField()
#     class Meta:
#         model = Wallet
#         fields = ['userId', 'amount']
#         read_only_fields =  ['userId', 'amount']
    
#     def get_userId(self, obj):
#         userId = str(obj.user_id)
#         return userId


# # Serialzer for registring a new user
# class RegisterSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=100)
#     email = serializers.EmailField(validators=[
#             UniqueValidator(
#                 queryset=CustomUser.objects.all(),
#                 message = 'Email already exists.'
                            
#             )
#         ])
#     password = serializers.CharField(max_length=100)

#     def validate(self, data):
#         password_pattern = "^(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

#         if not re.match(password_pattern, data['password']) : 
#             raise serializers.ValidationError('Weak password!' )
        
#         return data

# # Serializer for Login a new User
# class LoginSerializer(TokenObtainPairSerializer):

#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['username'] = user.username
#         token['email'] = user.email
#         token['email_verified'] = user.email_verified
#         token['phone_number'] = user.phone_number
#         token['phone_verified'] = user.phone_verified
#         token['first_name'] = user.first_name
#         token['last_name'] = user.last_name
#         token['profile_img'] = str(user.profile_img)
#         token['secret_code_status'] = user.secret_code_status
#         token['date_created'] = str(user.date_created)
#         token['bio'] = user.bio
        
        
#         return token


# class UserSerializer(serializers.ModelSerializer):
#     profile_img = serializers.SerializerMethodField()
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'email','first_name','last_name','email_verified', 'phone_verified',
#                   'phone_number', 'profile_img', 'bio','secret_code_status']
#         read_only_fields= ['id',]

#     def get_profile_img(self, obj):
#         request = self.context.get('request')
#         if obj.profile_img:
#             img_profile = obj.profile_img.url
#             return request.build_absolute_uri(img_profile)
#         else : None


# class PhoneNumberSerializer(serializers.Serializer):
#     #model = CustomUser
    
#     phone_number = serializers.CharField(required = True, max_length = 15)

#     def validate(self, data):
#         phone_regex = "^\+?1?\d{9,15}$"
        
#         if not re.match(phone_regex, data['phone_number']):
#             raise serializers.ValidationError('Incorrect number format!' )
        
#         return data

# class UserSecretSerializer(serializers.Serializer):
#     # model = CustomUser
#     def validate(self, data):
#         secret_regex = "^\+?1?\d{5}$"
#         if not re.match(secret_regex, data['secret_code']):
#             raise serializers.ValidationError('Incorrect secret format!' )
        
#         return data

# # Serializer for changing user password
# class ChangePasswordSerializer(serializers.Serializer): 
#     model = CustomUser

#     old_password = serializers.CharField(required = True, max_length = 255)
#     new_password = serializers.CharField(required = True, max_length = 255)

