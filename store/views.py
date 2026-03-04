from rest_framework.generics import ListCreateAPIView ,RetrieveAPIView ,ListAPIView
from store.models import Cart, CartItem, Category, Order, OrderItem, Product
from store.serializers import CartItemSerializer, CartSerializer, CategorySerializer, ProductSerializer
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
        
        serializer = CartItemSerializer(cart_item)
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

        serializer = CartItemSerializer(cart_item)
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

# class ViewCart(ListAPIView):
#     queryset = Cart.ob
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = CartItemSerializer

class ViewCart(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        cart = request.user.cart
        serializer = CartSerializer(cart)
        return Response(serializer.data,200)




class UpdateCartItemQuantityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def put(self,request):
        cart = request.user.cart
        product_id = request.data.get("product")
        quantity = request.data.get("quantity")

        try:
            quantity = int(quantity)
        except(TypeError,ValueError):
            return Response({"message": "Quantity must be a valid integer."}, status=400)
        
        if quantity < 0 :
            return Response({"message":"Quantity must be greater than zero."},status=400)
        
        product = get_object_or_404(Product,pk=product_id)
        cart_item = get_object_or_404(CartItem.objects.select_for_update(),cart=cart,product_id=product_id)

        old_quantity = cart_item.quantity
        new_quantity = quantity
        diff = new_quantity - old_quantity

        if new_quantity == 0:
            product.stock += old_quantity
            product.save()
            cart_item.delete()
            return Response({"message": "Item removed from cart"}, status=200)

        # If increasing quantity
        if diff > 0:
            if diff > product.stock:
                return Response(
                    {"message": "Not enough stock available."},
                    status=400
                )
            product.stock -= diff

        # If decreasing quantity
        elif diff < 0:
            product.stock += abs(diff)

        # Save updates
        cart_item.quantity = new_quantity
        cart_item.save()
        product.save()

        return Response(
            {"message": "Quantity updated successfully"},
            status=200
        )
        

class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self,request):
        cart = request.user.cart
        cart_items = cart.items.all()
        user = request.user


        if not cart_items.exists():
            return Response({"message":"Your cart is empty"},status=400)
        
        order = Order.objects.create(user=user,total_price=0)

        total = 0

        for item in cart_items:
            OrderItem.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity,
                price_at_purchase = item.product.price
            )
            total += item.product.price *item.quantity
            product = item.product
            if product.stock < item.quantity:
                return Response({"message":"sorry this Product isn't available with this quantity"},status=400)
            product.stock -= item.quantity
            product.save()
        
        order.total_price = total

        order.save()

        cart_items.delete()


        return Response({"message":"Order Created Successfully!"})

