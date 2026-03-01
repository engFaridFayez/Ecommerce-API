from rest_framework.generics import ListCreateAPIView ,RetrieveAPIView
from store.models import CartItem, Category, Product
from store.serializers import CartSerializer, CategorySerializer, ProductSerializer
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction



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


class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    

    def post(self,request):
        cart = request.user.cart 
        product = request.data.get("product")
        quantity = int(request.data.get("quantity",1))

        cart_item, created = CartItem.objects.get_or_create(cart=cart,product_id=product,defaults={"quantity":quantity})

        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        serializer = CartSerializer(cart_item)
        return Response(serializer.data,status=200)


class AddToCartViewPro(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self,request):
        cart = request.user.cart
        product_id= request.data.get("product")
        quantity = request.data.get("quantity",1)

        try:
            quantity = int(quantity)
        except(TypeError,ValueError):
            return Response({"message": "Quantity must be a valid integer."}, status=400)
        if quantity <= 0:
                return Response({"message":"Quantity must be greater than zero."},status=400)

        product = get_object_or_404(Product.objects.select_for_update(),pk=product_id)

        if product.is_active != True:
                return Response({"message":f"{product.name} is not available right now."},status=400)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart,product=product,defaults={"quantity":quantity})

        new_quantity = quantity if created else cart_item.quantity + quantity

        if new_quantity > product.stock:
            return Response(
                {"message": "Requested quantity exceeds available stock."},
                status=400
            )

        if not created:
            cart_item.quantity = new_quantity
            cart_item.save()

        serializer = CartSerializer(cart_item)
        return Response({
            "message": "Product added successfully",
            "cart_item": serializer.data
        },
        status=201 if created else 200)
    
class RemoveFromCart(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @transaction.atomic
    def delete(self,request):
        cart = request.user.cart
        product_id = request.data.get('product')

        cart_item = get_object_or_404(CartItem.objects.select_for_update(),product_id=product_id)

        product = cart_item.product

        product.stock += cart_item.quantity
        product.save()

        cart_item.delete()

        return Response({"message":f"product {product.name} removed from cart successfully"},status=200)
