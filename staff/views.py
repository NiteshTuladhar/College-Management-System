from django.shortcuts import render, redirect
from .forms import Edit_form_staff
from Accounts.models import Account
from django.contrib import messages
# Create your views here.
def edit_form_staff(request):

    account_info = Account.objects.get(id=request.user.id)
    account = Account.objects.latest('id')
    form = Edit_form_staff()

    if request.method == "POST":
        form = Edit_form_staff(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = account
            print(form.user)
            form.save()
            messages.success(request,"Staff Member Has been added.")
            return redirect('dashboard')

    context = {
        'form': form,
        'account_info' : account_info,
    }

    return render(request,'add_form/staff_edit_form.html',context)