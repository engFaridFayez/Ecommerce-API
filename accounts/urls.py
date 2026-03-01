from accounts import views
from django.urls import path
from accounts.custom_jwt_claims import CustomTokenObtainPairView

urlpatterns = [
    path('token/',CustomTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('register/',views.RegisterUser.as_view(),name='create-user'),
    path('user/profile/',views.UserProfile.as_view(),name='profile'),
    path('user/edit-profile/', views.EditProfile.as_view(), name='edit-profile'),
    path('user/delete-user/<int:pk>/', views.DeleteUser.as_view(), name='delete-user'),
]

