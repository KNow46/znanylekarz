from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.db.models import ForeignKey


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email adress')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

    def create_patient(self, email, password=None, **extra_fields):

        extra_fields['is_patient'] = True
        user = self.create_user(email, password, **extra_fields)
        Patient.objects.create(user=user)
        return user

    def create_doctor(self, email, password=None, specialization=None, license_number=None, city=None, **extra_fields):

        extra_fields['is_doctor'] = True
        user = self.create_user(email, password, **extra_fields)
        doctor = Doctor.objects.create(
            user=user,
            specialization=specialization,
            license_number=license_number,
            city=city
        )
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True)


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text="User's groups",
        verbose_name='Groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='User permissions',
        verbose_name='Permissions'
    )

    def __str__(self):
        return self.email

class Doctor(CustomUser):
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.specialization})"

class Patient(CustomUser):
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Opinion(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='opinions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='opinions')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Opinion by {self.patient} for {self.doctor}'


class Calendar(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)

class Appointment(models.Model):
    date = models.DateField()
    start = models.TimeField()
    duration = models.DurationField()
    calendar = ForeignKey(Calendar, on_delete=models.CASCADE)
    patient = models.ForeignKey(
        'Patient',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.date} {self.start} ({self.duration})"