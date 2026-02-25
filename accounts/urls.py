from accounts import views
from django.urls import path
from accounts.custom_jwt_claims import CustomTokenObtainPairView

urlpatterns = [
    path('token/',CustomTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('register/',views.RegisterUser.as_view(),name='create-user'),
]

