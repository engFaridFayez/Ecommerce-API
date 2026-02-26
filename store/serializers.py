from rest_framework import serializers

from store.models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name','description','price','stock','image','created_at','updated_at','is_active','slug','category')
        extra_kwargs = {'slug':{'read_only':True}}



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')