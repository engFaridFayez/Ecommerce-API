from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from accounts.models import CustomUser
from accounts.serializers import UserSerializer

# Create your views here.
class RegisterUser(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]