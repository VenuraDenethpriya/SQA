from django.shortcuts import render, redirect
from .models import Product, Patient, User
from django.shortcuts import get_object_or_404
from .forms import TransactionForm, TransactionProductForm, SignUpForm
from .models import Transaction, TransactionProduct
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from .models import Transaction, TransactionProduct
from .forms import TransactionProductFormSet
# Create your views here.
def home(request):
    return render(request, 'store/home.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('Logged out!'))
    return redirect('home')


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User not found. Please try again.")
            return redirect('login_user')
        
        # Check if the user is blocked
        if user.is_blocked:
            messages.error(request, "Your account is blocked due to multiple failed login attempts.")
            return redirect('login_user')
        
        # Check password
        if user.check_password(password):
            user.failed_attempts = 0  # Reset failed attempts on successful login
            user.save()
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect('home')
        else:
            user.failed_attempts += 1
            if user.failed_attempts >= 3:
                user.is_blocked = True
            user.save()
            messages.error(request, "Incorrect password. Please try again.")
            return redirect('login_user')
    return render(request, 'store/login_user.html')

            
def signin(request):
    return render(request,'store/signin.html', {})
    

def product(request):
    products = Product.objects.all()
    return render(request, 'store/product.html', {'products': products})

def patient(request):
    patients = Patient.objects.all()
    return render(request, 'store/patient.html', {'patients': patients})

def transaction(request):
    transactions = Transaction.objects.all()
    return render(request, 'store/transaction.html', {
        'transactions': transactions,
    })

# Add/edit/delete product
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        mrp = request.POST['mrp']
        mfg = request.POST['mfg']
        exp = request.POST['exp']
        qty = request.POST['qty']
        
        Product.objects.create(
            product_name=product_name,
            mrp=mrp,
            mfg=mfg,
            exp=exp,
            qty=qty
        )
        return redirect('product')
    return render(request, 'store/add_product.html', {})

def delete_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    product.delete()
    return redirect('product')
    

def edit_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == "POST":
        product.product_name = request.POST['product_name']
        product.mrp = request.POST['mrp']
        product.mfg = request.POST['mfg']
        product.exp = request.POST['exp']
        product.qty = request.POST['qty']
        product.save()
        return redirect('product')
    return render(request, 'store/edit_product.html', {'product': product})


# Add/edit/delete patient
def add_patient(request):
    if request.method == 'POST':
        patient_name = request.POST['patient_name']
        age = request.POST['age']
        sex = request.POST['sex']
        problem = request.POST['problem']
        customer_name = request.POST['customer_name']
        customer_age = request.POST['customer_age']
        nic = request.POST['nic']
        
        Patient.objects.create(
            patient_name = patient_name,
            age = age,
            sex = sex,
            problem = problem,
            customer_name = customer_name,
            customer_age = customer_age,
            nic = nic
        )
        return redirect('patient')
    return render(request, 'store/add_patient.html', {})

def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    patient.delete()
    return redirect('patient')
    
def edit_patient(request,  patient_id):
    patient =   get_object_or_404(Patient,  patient_id=patient_id)
    if request.method == "POST":
        patient.patient_name = request.POST['patient_name']
        patient.age = request.POST['age']
        patient.problem = request.POST['problem']
        patient.customer_name = request.POST['customer_name']
        patient.customer_age = request.POST['customer_age']
        patient.nic = request.POST['nic']
        patient.save()
        return redirect('patient')
    return render(request, 'store/edit_patient.html', {'patient': patient})
        
#Transaction
def add_transaction(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        product_formset = TransactionProductFormSet(request.POST)

        if transaction_form.is_valid() and product_formset.is_valid():
            # Save the transaction
            transaction = transaction_form.save()

            # Save each product in the formset and associate it with the transaction
            for form in product_formset:
                if form.cleaned_data:
                    transaction_product = form.save(commit=False)
                    transaction_product.transaction = transaction
                    transaction_product.save()

            # Redirect to the transaction page after saving
            return redirect('transaction')  # Ensure 'transaction' URL is correctly mapped in your urls.py
        else:
            return render(request, 'store/add_transaction.html', {
                'transaction_form': transaction_form,
                'formset': product_formset,
            })
    
    else:
        # GET request: Provide empty forms for transaction and product entry
        transaction_form = TransactionForm()
        product_formset = TransactionProductFormSet()

    return render(request, 'store/add_transaction.html', {
        'transaction_form': transaction_form,
        'formset': product_formset,
    })
      
    
def register(request):
    if  request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password2']
        User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )
        return redirect('login')
    return render(request, 'store/register.html')
