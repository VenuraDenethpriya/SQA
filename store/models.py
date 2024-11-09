from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254)
    password = models.CharField(
        _("Password"),
        max_length=128,
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$',
            message="Password must contain at least 6 characters with letters and numbers."
        )]
    )
    failed_attempts = models.IntegerField(default=0)
    is_blocked = models.BooleanField(default=False)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if it's a new user
            self.set_password(self.password)
        super().save(*args, **kwargs)
        
#Product
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    mfg = models.DateField(auto_now=False, auto_now_add=False)
    exp = models.DateField(auto_now=False, auto_now_add=False)
    qty = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product_name

#Patient
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=100)
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    problem = models.CharField(max_length=1000)
    customer_name = models.CharField(max_length=100)
    customer_age = models.IntegerField(MinValueValidator(19))
    nic = models.CharField(max_length=50)
    
    def __str__(self):
        return self.patient_name
  

#Transaction
class Transaction(models.Model):
    transaction_id = models.CharField(max_length=20, unique=True)
    date_time = models.DateTimeField()
    patient_name = models.ForeignKey("Patient", on_delete=models.DO_NOTHING, related_name='patient_transactions')
    customer_name = models.ForeignKey("Patient", on_delete=models.DO_NOTHING, related_name='customer_transactions')

    def __str__(self):
        return f"Transaction {self.transaction_id} for {self.patient_name}"

class TransactionProduct(models.Model):
    transaction = models.ForeignKey(Transaction, related_name='products', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def total_price(self):
        return self.quantity * self.unit_price

