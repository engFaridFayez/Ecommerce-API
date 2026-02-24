
from django.urls import path
from store import views


app_name = 'store'

urlpatterns = [
    path('products/',views.ProductListCreateView.as_view(),name='products'),
    path('products/<slug:slug>/',views.ProductDetailView.as_view(),name='product-detail'),
    path('categories/',views.CategoryListCreateView.as_view(),name='categories'),
]
