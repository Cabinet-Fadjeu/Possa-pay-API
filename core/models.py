# ----------------modele possa pay (Transaction) -----------
from django.db import models
import uuid
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from userAuth.models import CustomUser,Wallet,Service

RETREAT_STATE = (
    ("PENDING", "PENDING"),
    ("COMPLETED", "COMPLETED"),
    ("REJECTED", "REJECTED"),
)

# Create your models here.
class Retreat(models.Model):
    id  = models.UUIDField(_('id'),default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING ,null=True, blank=True)
    issuer = models.CharField(_('issuer'),max_length=250, null=True, blank=True)
    amount = models.DecimalField(_('Requested amount'), max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(_('last name',),max_length=5,blank=True, null=True)
    retreat_type =  models.CharField(_('Retreat Type'),max_length=250, null=True, blank=True)
    retreat_info =  models.TextField(null=True, blank=True)
    state = models.CharField(max_length=10, choices = RETREAT_STATE, default = 'PENDING', null=True, blank=True)
    request_date = models.DateTimeField(auto_now_add=True, verbose_name='request date',blank=True, null=True)
    issued_date = models.DateField(null=True, blank=True)

class Donation(models.Model):
    id  = models.UUIDField(_('id'),default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    first_name = models.CharField(_('first name',),max_length=250,blank=True, null=True)
    last_name = models.CharField(_('last name',),max_length=250,blank=True, null=True)
    email = models.EmailField(_('email',),max_length=250,blank=True)
    amount = models.DecimalField(_('User amount'), max_digits=10, decimal_places=2, blank=True, null=True)
    deposite_type = models.CharField(_('Deposite type'), max_length=250)
    is_Anonymous = models.BooleanField(_("Is anonymous"), default=False)

    deposite_date = models.DateTimeField(auto_now_add=True, verbose_name='recharge date',blank=True, null=True)

    def __str__(self) -> str:
        return self.email

class RechargeWallet (models.Model):
    id  = models.UUIDField(_('id'),default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING ,null=True, blank=True)
    account_email = models.EmailField(_('Account email'),max_length=250,null=True, blank=True)
    amount = models.DecimalField(_('User amount'), max_digits=10, decimal_places=2, blank=True, null=True)
    sender_email = models.EmailField(_('Sender email'),max_length=250,null=True, blank=True)
    recharge_method = models.CharField(_('recharge method'),max_length=250,blank=True, null=True)
    recharge_status = models.BooleanField(_("recharge status"), default=False)
    recharge_date = models.DateTimeField(auto_now_add=True, verbose_name='recharge date',blank=True, null=True)

    def __str__(self) :
        return str(self.account_email)
    
    def get_absolute_url(self):
        return "/transaction/%i/" % (self.id)


class Transfer(models.Model):
    id = models.UUIDField(_('id'),default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True)
    amount = models.DecimalField(_('User amount'), max_digits=10, decimal_places=2, blank=True, null=True)

    receiver_email = models.EmailField(_('receiver adress'),max_length=250)
    transfer_date = models.DateTimeField(auto_now_add=True, verbose_name='transfer date',blank=True, null=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self) :
        return str(self.user)

    def get_absolute_url(self):
        return "/transaction/%i/" % (self.id)
    

# ----------fin model possaPay (transaction) -----------------



# ----------------modele possa pay (cagnot) -----------


CAGNOTTE_STATUS = (
    ("ENCOURS", "Encours"),
    ("SOUMISSION", "Soumission"),
    ("PAYEE", "Payee"),
)

CURRENCY = (
    ("USD", "USD"),
    ("XAF", "XAF"),
    ("EUR", "EUR"),
)

WITHDRAWAL_METHODS = (
    ("CARTE_CREDIT", "Carte de Credit"),
    ("PAYPAL", "Paypal"),
    ("ORANGE_MONEY", "Orange Money"),
    ("MTN_MOMO", "MTN MoMo"),
)  

class Cagnotte(models.Model):
    id  = models.UUIDField(_('id'),default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,related_name='user_ID', null=True, blank=True)
 
    name_cagnotte = models.CharField(max_length=150, null=True, blank=True)
    code  = models.CharField(max_length=8, unique=True, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'")
    phone = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)

    chosen_currency = models.CharField(max_length=5, choices = CURRENCY, default = 'EUR', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    end_date = models.DateField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True, verbose_name='Date Joined',blank=True, null=True)

    cagnotte_status = models.CharField(max_length = 20, choices = CAGNOTTE_STATUS, default = 'ENCOURS')
    etat = models.BooleanField(default=True, null=True, blank=True)

    #withdrawal_method = models.CharField(max_length=100, choices = WITHDRAWAL_METHODS, default = 'CARTE_CREDIT')

    description = models.TextField(null=True, blank=True)
    # cagnotte_file = models.ImageField(upload_to="images/", null=True, blank=True)
    cagnotte_file = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        ordering = ('-date_created',)
    
    
    def __str__(self):
        return self.name_cagnotte

    
# Contribution for Pools
class ContributionCagnotte(models.Model):
    id  = models.UUIDField(_('id'),default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    cagnotte = models.OneToOneField(Cagnotte, unique=True, on_delete=models.CASCADE,related_name='cagnotte_ID', null=True, blank=True)
    contribution = models.DecimalField(max_digits=10, decimal_places=2,default=0.00, null=True, blank=True)
    currency = models.CharField(max_length=5, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True, verbose_name='Date Joined',blank=True, null=True)
    
    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return str(self.contribution)

# ----------------fin modele possa pay (cagnot) -----------

# ----------------modele possa pay (Participant) -----------



# from cagnotte.models import Cagnotte

CURRENCY = (
    ("USD", "USD"),
    ("XAF", "XAF"),
    ("EUR", "EUR"),
)

CONTRIBUTION_METHODS = (
    ("CARTE_CREDIT", "Carte de Credit"),
    ("PAYPAL", "Paypal"),
    ("ORANGE_MONEY", "Orange Money"),
    ("MTN_MOMO", "MTN MoMo"),
    ("SMALL_POSSA", "Small Possa"),
)  
# TRANSACTION_STATUS = (
#     ("FAILED", "Failed"),
#     ("SUCCESS", "Success"),
#     ("PENDING", "Pending"),
#     ("CANCELLED", "Cancelled"),
# )

PAYMENT_STATUS = (
    ('UNPAID', 'Unpaid'),
    ('PAID', 'Paid'),
    ('CANCELLED', 'Cancelled'),
)

RETREAT_STATUS = (
    ('UNHANDLED', 'Unhandled'),
    ('HANDLED', 'Handled'),
    ('CANCELLED', 'Cancelled'),
)
# Create your models here.
class Participant(models.Model):
    id  = models.UUIDField(_('id'), default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    pool = models.ForeignKey(Cagnotte,on_delete=models.CASCADE)
    transaction_status = models.CharField(max_length=15, choices = PAYMENT_STATUS, default = 'UNPAID', blank=True, null=True)
   
    f_name_participant = models.CharField(_('Participant F_Name'),max_length=150,null=True, blank=True)
    l_name_participant = models.CharField(_('Participant L_Name'),max_length=150,null=True, blank=True)
    email_participant = models.EmailField(_('Participant Email'),max_length=250, null= True, blank=True)
    
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'")
    phone_number = models.CharField(_('Phone Number'),validators=[phone_regex], max_length=17, blank=True,null=True)
    

    amount = models.DecimalField(_('Contribution'), max_digits=10, decimal_places=2, blank=True, null=True)
    contribution_method = models.CharField(max_length=100, choices = CONTRIBUTION_METHODS, default = 'CARTE_CREDIT')
    currency = models.CharField(max_length=5, choices = CURRENCY, default = 'EUR', null=True, blank=True)
    

    is_Anonymous = models.BooleanField(_('Is Anonymous'),default=False)

    date_participate = models.DateTimeField(_('Date Participated'),auto_now_add=True)

    class Meta:
        ordering = ['-date_participate',]
    
    def __str__(self):
        return self.email_participant
 
class PoolRetreat(models.Model):
    id = models.UUIDField(_('id'), default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    pool = models.ForeignKey(Cagnotte,on_delete=models.CASCADE)
    retreat_status = models.CharField(_('Retreat Status'), max_length=15, choices = RETREAT_STATUS, default = 'UNHANDLED', blank=True, null=True)
    entered_amt = models.DecimalField(_('Entered Amount'), max_digits=10, decimal_places=2, blank=True, null=True)
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=5, choices = CURRENCY, default = 'EUR', null=True, blank=True)
    commission = models.DecimalField(_('Commission'), max_digits=10, decimal_places=2, blank=True, null=True)
    date_created = models.DateTimeField(_('Date Completed'),auto_now_add=True)
    date_handled = models.DateTimeField(_('Date Completed'),auto_now_add=False, null=True, blank=True) 
    requestor_email = models.EmailField(_('Requestor email'), blank=True, null=True)

    class Meta:
        ordering = ['-date_created',]
# ----------------finmodele possa pay (Participant) -----------

# ----------------modele possa pay (debut review) -----------


# Create your models here.


class Review(models.Model):
    id  = models.UUIDField(_('id'), default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(_('Name'), max_length = 100, null=True, blank=True)
    title = models.CharField(_('Title'), max_length = 100, null=True, blank=True)
    description = models.TextField(_('Description'),null=True, blank= True)
    profile_img = models.ImageField(upload_to="reviews/", null=True, blank=True,default=None)
    date_created = models.DateTimeField(_('Date created'),auto_now_add=True)


    class Meta:
        ordering = ['-date_created']

    def __str__(self) -> str:
        return self.name
    


class ExchageRate(models.Model):
    id  = models.UUIDField(_('id'), default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    base = models.CharField(_('Base'), max_length = 6, null=True, blank=True)
    rates = models.CharField(_('Rates'), max_length = 5, null=True, blank=True)
    values = models.CharField(_('Values'), max_length = 5, null=True, blank=True)
    date_created = models.DateTimeField(_('Date created'),auto_now_add=True)


# ----------------modele possa pay (fin review) -----------



class Transaction(models.Model):
    id = models.UUIDField(_('Transaction ID'), default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    sender_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="sent_transactions", blank=True, null=True)
    recipient_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="received_transactions", blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="service_transactions", blank=True, null=True)
    
    amount = models.DecimalField(_('Transaction Amount'), max_digits=10, decimal_places=2)
    status = models.CharField(_('Transaction Status'), max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    transaction_type = models.CharField(_('Transaction Type'), max_length=20, choices=[('user_to_user', 'User to User'), ('service_payment', 'Service Payment')], default='user_to_user')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date Created')
    
    def __str__(self):
        return f"Transaction {self.id} - {self.status} - {self.amount} USD"

    def execute_transaction(self):
        """Exécute la transaction en vérifiant le solde de l'expéditeur et en transférant le montant au destinataire ou au service."""
        if self.sender_wallet and self.sender_wallet.amount >= self.amount:
            # Débiter l'expéditeur
            self.sender_wallet.amount -= self.amount
            self.sender_wallet.save()

            # Créditer le destinataire ou le portefeuille lié au service
            if self.transaction_type == 'user_to_user' and self.recipient_wallet:
                self.recipient_wallet.amount += self.amount
                self.recipient_wallet.save()
            elif self.transaction_type == 'service_payment' and self.service:
                self.service.user.wallet.amount += self.amount
                self.service.user.wallet.save()

            # Marquer la transaction comme terminée
            self.status = 'completed'
            self.save()
        else:
            self.status = 'failed'
            self.save()

