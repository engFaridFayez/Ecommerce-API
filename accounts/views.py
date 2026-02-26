from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from accounts.models import CustomUser
from accounts.serializers import RegisterSerializer, UserSerializer

# Create your views here.
class RegisterUser(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]