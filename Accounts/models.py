from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

gender_list = [('Male', 'male'), ('Female', 'female')]


class AccountManager(BaseUserManager):
    def create_user(self, email, date_of_birth, full_name, image, address, gender, contact_no, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),

            date_of_birth=date_of_birth,
            full_name=full_name,
            image=image,
            address=address,
            gender=gender,
            contact_no=contact_no
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, address, gender, contact_no, password=None):
        user = self.create_user(
            email,

            password=password,
            date_of_birth=None,
            full_name=full_name,
            image=None,
            address=address,
            gender=gender,
            contact_no=contact_no
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(blank=True, null=True, )
    full_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='user/', blank=True, null=True)
    address = models.CharField(max_length=100)
    gender = models.CharField(max_length=30, choices=gender_list)
    contact_no = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    is_admin = models.BooleanField(default=False, blank=True, null=True)
    is_faculty = models.BooleanField(default=False, blank=True, null=True)
    is_first_login = models.BooleanField(default=True, blank=True, null=True)
    is_student = models.BooleanField(default=False, blank=True, null=True)
    is_teacher = models.BooleanField(default=False, null= True, blank=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'address', 'gender', 'contact_no']

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url