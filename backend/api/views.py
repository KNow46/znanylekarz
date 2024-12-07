from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import  Doctor
from .serializers import  DoctorSerializer, DoctorPostSerializer
from django.shortcuts import get_object_or_404

class DoctorListView(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return DoctorPostSerializer
        return super().get_serializer_class()
    #
    # def post(self, request):
    #     serializer_class = DoctorPostSerializer
    #     return super().post(request)

# class DoctorListView(APIView):
#     def get(self, request, id=None):
#         if id is None:
#             doctor = Doctor.objects.all()
#             serializer = DoctorSerializer(doctor, many=True)
#         else:
#             doctor = get_object_or_404(Doctor, id=id)
#             serializer = DoctorSerializer(doctor)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = DoctorPostSerializer



