from rest_framework import serializers

from store.models import Cart, CartItem, Category, Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','description','price','stock','image','created_at','updated_at','is_active','slug','category')
        extra_kwargs = {'slug':{'read_only':True}}



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    cart = serializers.StringRelatedField()


    class Meta:
        model = CartItem
        fields = ['cart','product','quantity','total_price']

    def get_total_price(self,obj):
        return obj.product.price * obj.quantity
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Cart
        fields = ['user','created_at','items']
        read_only_fields = ('user','created_at')
    


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=OrderItem
        fields = ['order','product','quantity','price_at_purchase']
        read_only_fields = ('order',)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,read_only=True)

    class Meta:
        model=Order
        fields = ["id","total_price","status","created_at","items"]

    