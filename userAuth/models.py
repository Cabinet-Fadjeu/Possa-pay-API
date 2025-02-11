# ---------------- modele possa pay (user) -----------
from django.db import models

from django.contrib.auth.models import  AbstractUser
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
import uuid
import secrets  # Pour générer les clés publiques et secrètes

# from django_cryptography.fields import encrypt



# Import for password reset
from django.dispatch import receiver
#from django.urls import reverse
# from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail 

# Importing user manager
from .managers import CustomUserManager


CURRENCY = (
    ("USD", "USD"),
    ("XAF", "XAF"),
    ("EUR", "EUR"),
)

class CustomUser(AbstractUser):
    id  = models.UUIDField(_('id'),default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(_('email adress'),unique= True,max_length=250)
    email_verified = models.BooleanField(_("Email verified"), default=False)
    email_OTP = models.CharField(_("Email OTP"), max_length=7, blank=True, null=True)

    username = models.CharField(_('username'),max_length=250,blank=True, null=True)
    password = models.CharField(_('password'),max_length=255)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True,null=True)
    phone_verified = models.BooleanField(_("Phone Verified"), default=False)
    phone_OTP = models.CharField(_("Phone OTP"), max_length=5, blank=True,null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    secret_code = models.CharField(_("Secret Code"), max_length=255, blank=True, null=True)
    secret_code_status = models.BooleanField(_("Secret code set"), default=False, blank=True, null=True)
    is_company = models.BooleanField(default=False, blank=True, null=True)  # Ajout du champ pour distinguer les entreprises des utilisateurs réguliers
    profile_img = models.ImageField(upload_to='profiles',blank=True, null=True)
    bio = models.TextField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date Joined',blank=True, null=True)


    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)


    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    

class Wallet(models.Model):
    id  = models.UUIDField(_('id'),default=uuid.uuid4, unique=True,primary_key=True,  editable=False)
    user_id = models.OneToOneField(CustomUser,on_delete=models.CASCADE,blank=True, unique=True, null=True)
    amount = models.DecimalField(_('User amount'), max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    devise = models.CharField(choices=CURRENCY, max_length=5,blank=True, null=True, default="XAF")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date Created',blank=True, null=True)
    
    def __str__(self):
        return ('amount : '  +  str(self.amount))
    
    def deposit(self, amount):
        """Ajoute un montant au portefeuille de l'utilisateur."""
        self.amount += amount
        self.save()

class Compte(models.Model):
    id  = models.UUIDField(_('id'),default=uuid.uuid4, unique=True,primary_key=True,  editable=False)
    # service_id = models.OneToOneField(CustomUser,on_delete=models.CASCADE,blank=True, unique=True, null=True)
    amount = models.DecimalField(_('User amount'), max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date Created',blank=True, null=True)
    
    def __str__(self):
        return ('amount : '  +  str(self.amount))
    
    def deposit(self, amount):
        """Ajoute un montant au portefeuille de l'utilisateur."""
        self.amount += amount
        self.save()


class Service(models.Model):
    id = models.UUIDField(_('id'), default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(_('Service Name'), max_length=255)
    description = models.TextField(_('Service Description'), blank=True, null=True)
    public_key = models.CharField(_('Public Key'), max_length=64, unique=True, default=secrets.token_hex(32))
    secret_key = models.CharField(_('Secret Key'), max_length=64, unique=True, default=secrets.token_hex(32))
    compte = models.OneToOneField(Compte, on_delete=models.CASCADE, null=True, blank=True)
    allowed_hosts = models.TextField(help_text="Liste de domaines autorisés, séparés par des virgules", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date Created', blank=True, null=True)

    def __str__(self):
        return f"Service: {self.name} - Public Key: {self.public_key}"

    def receive_payment(self, amount):
        """Effectue un dépôt dans le portefeuille de l'utilisateur associé au service."""
        wallet = Wallet.objects.get(user_id=self.user)
        wallet.deposit(amount)

    def save(self, *args, **kwargs):
        if not self.public_key:
            self.public_key = uuid.uuid4().hex  # Générer une clé publique unique
            print('public',self.public_key)
        if not self.secret_key:
            self.secret_key = uuid.uuid4().hex  # Générer une clé secrète unique
            print('public',self.public_key)
        super(Service, self).save(*args, **kwargs)

# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

#     #email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
#     message_body = "Your Passcode is : " + reset_password_token.key

#     send_mail(
#         # title:
#         "Password Reset from {title}".format(title="Small Possa"),
#         # message:
#         #email_plaintext_message,
#         message_body,
#         # from:
#         "SmallPossa@gmail.com",
#         # to:
#         [reset_password_token.user.email]
#     )    


# ----------------fin modele possa pay (user) -----------




