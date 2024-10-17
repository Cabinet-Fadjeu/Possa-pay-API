from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Modèle Utilisateur personnalisé
class User(AbstractUser):
    # Ajoutez ici des champs supplémentaires si nécessaire
    is_company = models.BooleanField(default=False)  # Si l'utilisateur est une entreprise
    is_admin = models.BooleanField(default=False)    # Si l'utilisateur est un admin

    def __str__(self):
        return self.username


# Modèle pour les entreprises
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Chaque entreprise est liée à un utilisateur
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


# Modèle Wallet (Portefeuille)
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Solde du wallet

    def __str__(self):
        return f"{self.user.username} - {self.balance}€"

    # Fonction pour ajouter de l'argent au wallet
    def deposit(self, amount):
        self.balance += amount
        self.save()

    # Fonction pour retirer de l'argent du wallet
    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False


# Modèle pour les transactions
class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} : {self.amount}€"

    # Fonction pour effectuer une transaction
    def process_transaction(self):
        sender_wallet = self.sender.wallet
        receiver_wallet = self.receiver.wallet

        if sender_wallet.withdraw(self.amount):  # Si l'utilisateur a assez d'argent
            receiver_wallet.deposit(self.amount)  # On crédite le wallet du récepteur
            return True
        return False

