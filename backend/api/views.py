from operator import truediv

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Doctor, Appointment, Patient, Opinion, CustomUser, CustomToken
from .permissions import IsDoctor
from .serializers import DoctorSerializer, DoctorPostSerializer, AppointmentSerializer, PatientSerializer, \
    PatientPostSerializer, OpinionSerializer, EmailAuthSerializer
from drf_yasg import openapi

class DoctorView(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return DoctorPostSerializer
        return super().get_serializer_class()

    def list(self, request):
        return super().list(request)

def getIsDoctor(userId):
    try:
        Doctor.objects.get(id=userId)
        return True
    except Doctor.DoesNotExist:
        return False


class AppointmentView(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_fields = ['doctor', 'patient', 'date']
    filter_backends = [DjangoFilterBackend]


    def create(self, request, *args, **kwargs):
        user = get_object_or_404(CustomToken, token=request.COOKIES.get('authToken')).user
        doctor = get_object_or_404(Doctor, id=user.id)
        print(getIsDoctor(user.id))

        serializer = AppointmentSerializer(data={**request.data, 'doctor': doctor})

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def list(self, request, *args, **kwargs):
    #     pass



class PatientView(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return PatientPostSerializer
        return super().get_serializer_class()

class OpinionView(ModelViewSet):
    queryset = Opinion.objects.all()
    serializer_class = OpinionSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_fields = ['doctor', 'patient']

def authenticate(email, password):
    user = get_object_or_404(CustomUser, email=email, password=password)
    token, created = CustomToken.objects.get_or_create(user=user)
    return token

def getUser(authToken):
    user = CustomToken.objects.get(token=authToken).user

    if isinstance(user, Doctor):
        print('Doctor')
    elif isinstance(user, Patient):
        print('Patient')
    else:
        print('Unknown')

    return user.id


class EmailAuthToken(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=EmailAuthSerializer,
        responses={
            200: openapi.Response('Token generated', examples={'application/json': {'token': 'example_token'}}),
            400: openapi.Response('Invalid credentials', examples={'application/json': {'error': 'Invalid credentials'}})
        }
    )
    def post(self, request, *args, **kwargs):
        # print(isDoctor(getUser(request.headers['authToken'])))

        serializer = EmailAuthSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            token = authenticate(email=email, password=password)

            if token:
                userId = getUser(token.token)
                isDoctor = getIsDoctor(userId)
                return Response({'token': token.token,
                                 'isDoctor': isDoctor})

            return Response({'error': 'Invalid credentials'}, status=400)
        return Response(serializer.errors, status=400)

class CheckTokenView(APIView):
    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'authToken',
    #             openapi.IN_HEADER,
    #             description="Autorization token",
    #             type=openapi.TYPE_STRING,
    #             required=True,
    #         )
    #     ]
    # )
    def get(self, request, *args, **kwargs):
        print(request.COOKIES)
        #token = request.COOKIES.get('authToken')
        token = get_object_or_404(CustomToken, token=request.COOKIES.get('authToken'))

        isDoctor = getIsDoctor(token.user.id)

        return Response({'user_id': token.user.id, 'is_doctor': isDoctor})
