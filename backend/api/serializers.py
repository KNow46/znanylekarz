from rest_framework import serializers
from .models import Doctor, Appointment, Patient, Opinion


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        rating = serializers.Field()
        model = Doctor
        fields = ['id', 'rating','first_name', 'last_name', 'email', 'phone_number', 'is_active',
                  'phone_number','date_joined', 'specialization', 'city', 'license_number']

class DoctorPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields =  ['id','password', 'first_name', 'last_name', 'email', 'is_active',
                  'phone_number', 'date_joined', 'specialization', 'city', 'license_number']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'is_active',
                  'phone_number','date_joined']

class PatientPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'password', 'first_name', 'last_name', 'email', 'phone_number', 'is_active',
                  'phone_number', 'date_joined']

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(many=False, required=False)
    class Meta:
        model = Appointment
        fields = '__all__'

class OpinionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opinion
        fields = '__all__'

class EmailAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

