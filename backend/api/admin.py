from django.contrib import admin
from .models import CustomUser, Doctor, Patient, Opinion


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_doctor', 'is_patient', 'is_active')
    search_fields = ('email',)

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Opinion)
