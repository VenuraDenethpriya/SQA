from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register',views.register, name='register'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('login',views.login_user, name='login_user'),

    
    path('products', views.product, name="product"),
    path('patients', views.patient, name="patient"),
    path('transaction', views.transaction, name="transaction"),
    
    path('add_transaction', views.add_transaction, name="add_transaction"),
    path('add_product', views.add_product, name="add_product"),
    path('add_patient', views.add_patient, name="add_patient"),   
     
    path('delete_product/<int:product_id>/', views.delete_product, name="delete_product"),
    path('delete_patient/<int:patient_id>/', views.delete_patient, name="delete_patient"),
    
    path('edit_product/<int:product_id>', views.edit_product, name="edit_product"),
    path('edit_patient/<int:patient_id>/', views.edit_patient, name="edit_patient"),
    

]