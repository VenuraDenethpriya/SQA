from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 
from .models import Transaction, TransactionProduct, Product
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
import re


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        
        if len(password1) < 6:
            raise ValidationError("Password must be at least 6 characters long.")
        
        if not re.search(r'[A-Za-z]', password1):
            raise ValidationError("Password must contain at least one letter.")
        
        if not re.search(r'[a-z]', password1):
            raise ValidationError("Password must contain at least one lowercase letter.")
        
        if not re.search(r'[A-Z]', password1):
            raise ValidationError("Password must contain at least one uppercase letter.")
        
        if not re.search(r'[0-9]', password1):
            raise ValidationError("Password must contain at least one number.")
        
        if not re.search(r'[\W_]', password1):
            raise ValidationError("Password must contain at least one special character (e.g., @, #, $, %, etc.).")
        
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        # Check if passwords match
        if password1 and password2 and password1 != password2:
            raise ValidationError("The two passwords do not match.")
        
        return password2







# Wrong code
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