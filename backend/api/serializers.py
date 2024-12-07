from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'is_active',
                  'phone_number','date_joined', 'specialization', 'city', 'license_number']

class DoctorPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
            # ['id','password', 'first_name', 'last_name', 'email', 'is_active',
            #       'phone_number', 'date_joined', 'specialization', 'city', 'license_number']