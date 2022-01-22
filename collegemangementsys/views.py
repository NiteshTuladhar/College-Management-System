from django.shortcuts import render
from Accounts.decorators import *

@unauthenticated_user
def homepage(request):

	context = {}

	return render (request,'logins.html',context)