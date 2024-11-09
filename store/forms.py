from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 
from .models import Transaction, TransactionProduct, Product
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
import re

class TransactionForm(forms.ModelForm):
    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'date_time', 'patient_name', 'customer_name']

class TransactionProductForm(forms.ModelForm):
    product_name = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        empty_label="Select a product",
        widget=forms.Select
    )

    class Meta:
        model = TransactionProduct
        fields = ['product_name', 'quantity', 'unit_price']

# Formset for multiple products
TransactionProductFormSet = modelformset_factory(
TransactionProduct, form=TransactionProductForm, extra=1
    )

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2']

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        
        # Ensure the password is at least 6 characters and contains both letters and numbers
        if len(password1) < 6:
            raise ValidationError("Password must be at least 6 characters long.")
        if not re.search(r'[A-Za-z]', password1):
            raise ValidationError("Password must contain at least one letter.")
        if not re.search(r'[0-9]', password1):
            raise ValidationError("Password must contain at least one number.")
        
        return password1
