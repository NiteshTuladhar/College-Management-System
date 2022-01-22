from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .models import Account
from notices.models import NoticeBoard
from student.models import *
from teacher.models import *
from staff.models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import HttpResponseRedirect
from .form import Add_New_User
from .mail import CustomMail
from .token import generatetoken
from teacher import views
from .decorators import unauthenticated_user, authenticated_user
# Create your views here.


@unauthenticated_user
def register(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		full_name = request.POST['full_name']
		address = request.POST['address']
		contact_no = request.POST['contact_no']
		gender = request.POST['gender']
		if(len(password)>6):
			account = Account(email=email,full_name=full_name,address=address,contact_no=contact_no, gender=gender)
			account.set_password(password)
			try:
				account.save()
				messages.success(request,message="Account Created Successfully")
				return redirect('login')
			except:
				messages.error(request,"Email already exist")
		else:
			messages.error(request,message="Password must be more than 6 character long")
			return redirect('register')
	else:
		return render(request,'signup.html')

@unauthenticated_user
def userlogin(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(request,email=email,password=password)
		if user is not None:
			login(request, user)
			account = Account.objects.get(id=request.user.id)
			is_first_login = account.is_first_login
			if is_first_login:
				return redirect('newpassword')
			else:
				if account.is_admin:
					return redirect('dashboard')
				elif account.is_teacher:
					print('Teacher')
					return redirect('teacher_homepage')
				elif account.is_student:
					print('Student')
					return redirect('student_homepage')
				else:
					pass

		else:
			messages.error(request,"Email or Password does not match")
			return redirect('login')
	else:
		return render(request,'logins.html')


def logouts(request):
	logout(request)
	return redirect('login')

def newpassword(request):
	if request.method == "POST":
		password = request.POST['new_password']
		confirm_password = request.POST['confirm_password']

		if password == confirm_password:
			account = Account.objects.get(id=request.user.id)
			account.set_password(password)
			account.is_first_login = False
			account.save()
			return redirect('dashboard')
			
	context = {

	}
	return render(request, 'newpassword.html', context)
	
@authenticated_user
def dashboard(request):


	account_info = Account.objects.get(id=request.user.id)	


	account_info = Account.objects.get(id=request.user.id)	

	teacher = Teacher.objects.all().count()
	student = Student.objects.all().count()
	staff = Staff.objects.all().count()
	course= Course.objects.all().count()
	faculty = Faculty.objects.all().count()
	notices = NoticeBoard.objects.all().order_by('-notice_date')[:5]
	notice_count = notices.count()
	print(notice_count)

	print('--------------------countdjhfjaksdfh---------------')
	context = {
		'homecurrent':'current',
		'account_info' : account_info,
		'teacher':teacher,
		'student': student,
		'staff': staff,
		'course':course,
		'faculty': faculty,
		'notices' : notices,
		'notice_count' : notice_count,
	}
	return render(request, 'homepage/homepage.html', context)


def add_new_account(request):

	account_info = Account.objects.get(id=request.user.id)
	notices = NoticeBoard.objects.all().order_by('-notice_date')[:5]
	notice_count = notices.count()
	form = Add_New_User()
	if request.method == "POST":
		form = Add_New_User(request.POST or None)
		if form.is_valid():
			form = form.save(commit=False)
			password = generatetoken()
			form.set_password(password)
			name = request.POST['full_name']
			email = request.POST['email']

			student = request.POST['is_student']
			teacher = request.POST['is_teacher']
			staff = request.POST['is_faculty']
			mail = CustomMail('mail/account_creation.html', 'New Account Creation', [email],full_name=name,password=password, email=email)
			mail.push()
			print("Mail Sent")

			try:
				if student == 'true' and teacher == "true" and staff == "true":
					messages.warning(request, message = "THE USER CAN'T BE STUDENT, TEACHER and STAFF")
					return redirect('add_new_account')
				elif student == 'true' and teacher == 'true':
					messages.warning(request, message="THE USER CAN'T BE STUDENT AND TEACHER")
					return redirect('add_new_account')
				elif student == 'true' and staff == 'true':
					messages.warning(request, message="THE USER CAN'T BE STUDENT AND STAFF")
					return redirect('add_new_account')
				elif teacher == 'true' and staff == 'true':
					messages.warning(request, message="THE USER CAN'T BE TEACHER AND STAFF")
					return redirect('add_new_account')
				else:
					form.save()
			except:
				pass
			if student == 'true':
				return redirect('editform_student')
			elif teacher == "true":
				return redirect('teacher_edit_form')
			elif staff == 'true':
				return redirect('staff_edit_form')
			else:
				return False


	context = {
		'addcurrent':'current',
		'form': form,
		'account_info' : account_info,
		'notice_count' : notice_count,
	}
	return render(request, 'add_form/add_new_account.html', context)



def change_dp(request):

	account_info = Account.objects.get(id=request.user.id)
	user_id = request.user.id

	if request.method == 'POST':
		account_info = Account.objects.get(id=request.user.id)
		image = request.FILES.get('profile_image')

		account_info.image = image
		account_info.save()

		messages.success(request,message='Your Profile Image Has Been Changed.')
		
	context = {

		'account_info' : account_info,
	}

	return render(request,'change_display_picture.html',context)




