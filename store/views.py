from rest_framework.generics import ListCreateAPIView ,RetrieveAPIView

from store.models import Category, Product
from store.serializers import CategorySerializer, ProductSerializer



class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['category','category__slug']
    search_fields = ['name','description']

class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class= None

class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
