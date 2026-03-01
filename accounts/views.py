from rest_framework.generics import CreateAPIView ,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.permissions import AllowAny
from accounts.models import CustomUser, Profile
from accounts.serializers import  DeleteUserSerializer, ProfileSerializer, RegisterSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.parsers import (MultiPartParser,FormParser)
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class RegisterUser(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class DeleteUser(DestroyAPIView):
    queryset= CustomUser.objects.all()
    serializer_class = DeleteUserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

class UserProfile(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile
    
class EditProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [FormParser,MultiPartParser]

    def put(self,request,format=None):
        profile = request.user.profile
        serializer = ProfileSerializer(instance=profile,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=200)
        else:
            return Response(data=serializer.errors,status=400)
        