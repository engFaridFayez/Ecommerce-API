from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from accounts.custom_jwt_claims import CustomTokenObtainPairView

urlpatterns = [
    path('token/',CustomTokenObtainPairView.as_view(),name='token_obtain_pair'),
]

