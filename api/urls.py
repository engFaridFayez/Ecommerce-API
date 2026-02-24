from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/',include("store.urls")),
    path('store/',include('accounts.urls')),
]
