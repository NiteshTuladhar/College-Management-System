from django.urls import path
from . import views



urlpatterns =[
    path('create_payment_info/',views.createPaymentInfo, name='createpayment'),
    path('list_payment_info/',views.listPaymentInfo, name='listpayment'),

    path('mypayments/', views.payments,name='payment'),
    path('makepayment/<int:id>', views.makePayment,name='makepayment'),
    path('process_payment/<int:id>',views.getAmount, name='getamount'),
    path('success/<int:id>', views.esewa, name='esewa_success'),
    path('payment_edit/<int:id>', views.payment_edit, name='payment_edit'),
    path('payment_delete/<int:id>', views.payment_delete, name='payment_delete'),

    
] 