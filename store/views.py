from django.shortcuts import render, redirect
from .models import Product, Patient, User, NewTransaction
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
import csv
from django.http import HttpResponse
from django.urls import reverse


# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products':products})

def login_user(request):
    if 'attempts' not in request.session:
        request.session['attempts'] = 0

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['attempts'] = 0
            messages.success(request, "You have been logged in.")
            return redirect('home')
        else:
            request.session['attempts'] += 1

            if request.session['attempts'] == 3:
                messages.error(request, "Your account is blocked due to 3 failed login attempts.")
                return redirect('home')

            else:
                messages.error(request, "Username or Password incorrect. Please try again.")

            return redirect('login_user')

    return render(request, 'store/login.html')

            
def signin(request):
    return render(request,'store/signin.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('Logged out!'))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data["username"]
            password= form.cleaned_data["password1"]
            #log in user
            user =authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ("You have registered! Welcome!!!"))
            return redirect('home')
        else:
            messages.success(request, ("threre is a problemregistering, try agaian"))
            return redirect('home')
    else:
        return render(request,'store/register_user.html', {'form': form})





 # Show/Add/edit/delete product   
def product(request):
    products = Product.objects.all()
    return render(request, 'store/product.html', {'products': products})

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
        messages.success(request, ("You have succussfully added new product"))
        return redirect('product')
    return render(request, 'store/add_product.html', {})

def edit_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == 'POST':
        product.product_name = request.POST.get('product_name', product.product_name)
        product.mrp = request.POST.get('mrp', product.mrp)
        product.mfg = request.POST.get('mfg', product.mfg)
        product.exp = request.POST.get('exp', product.exp)
        product.qty = request.POST.get('qty', product.qty)
        product.save()
        return redirect(reverse('edit_product', args=[product_id]))
    return render(request, 'store/edit_product.html', {'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    product.delete()
    messages.error(request, ("You have succussfully delete a product"))
    return redirect('product')






# Show/Add/edit/delete patient
def patient(request):
    patients = Patient.objects.all()
    return render(request, 'store/patient.html', {'patients': patients})

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
        messages.success(request, ("You successfully added new patient"))
        return redirect('patient')
    return render(request, 'store/add_patient.html', {})

def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    patient.delete()
    messages.error(request, ("You have succussfully delete a patient"))
    return redirect('patient')
    
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    if request.method == "POST":
        patient.patient_name = request.POST.get('patient_name', patient.patient_name)
        patient.age = request.POST.get('age', patient.age)
        patient.problem = request.POST.get('problem', patient.problem)
        patient.customer_name = request.POST.get('customer_name', patient.customer_name)
        patient.customer_age = request.POST.get('customer_age', patient.customer_age)
        patient.nic = request.POST.get('nic', patient.nic)
        patient.save()
        return redirect(reverse('edit_patient', args=[patient_id]))
    return render(request, 'store/edit_patient.html', {'patient': patient})





#Transaction
def transaction_form(request):
    patients = Patient.objects.all()
    if request.method == 'POST':
        patient_name = request.POST['patient_name']
        patient_age = request.POST['patient_age']
        problem = request.POST['problem']
        products = request.POST['products']
        customer_name = request.POST['customer_name']
        customer_age = request.POST['customer_age']
        
        NewTransaction.objects.create(
            patient_name=patient_name,
            patient_age=patient_age,
            problem=problem,
            products=products,
            customer_name=customer_name,
            customer_age=customer_age
        )
        return redirect('transaction_history')
    return render(request, 'store/transaction_form.html', {'patients':patients})


def transaction_history(request):
    newTransactions = NewTransaction.objects.all()
    return render(request, 'store/transaction_history.html', {'newTransactions':newTransactions}) 


def generate_transaction_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transaction_report.csv"'
    
    writer = csv.writer(response)
    
    writer.writerow(['ID', 'Date/Time', 'Patient Name', 'Patient Age', 'Problem', 'Products', 'Customer Name', 'Customer Age'])
    
    transactions = NewTransaction.objects.all()
    
    for transaction in transactions:
        writer.writerow([
            transaction.transaction_id,
            transaction.datetime,
            transaction.patient_name,
            transaction.patient_age,
            transaction.problem,
            transaction.products,
            transaction.customer_name,
            transaction.customer_age,
        ])
    
    return response









# Wrong code
def transaction(request):
    transactions = Transaction.objects.all()
    return render(request, 'store/transaction.html', {
        'transactions': transactions,
    })


def add_transaction(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        product_formset = TransactionProductFormSet(request.POST)

        if transaction_form.is_valid() and product_formset.is_valid():
            transaction = transaction_form.save()

            for form in product_formset:
                if form.cleaned_data:
                    transaction_product = form.save(commit=False)
                    transaction_product.transaction = transaction
                    transaction_product.save()
            return redirect('transaction')
        else:
            return render(request, 'store/add_transaction.html', {
                'transaction_form': transaction_form,
                'formset': product_formset,
            })
    
    else:
        transaction_form = TransactionForm()
        product_formset = TransactionProductFormSet()

    return render(request, 'store/add_transaction.html', {
        'transaction_form': transaction_form,
        'formset': product_formset,
    })
      
    