from rest_framework import serializers
from .models import Inventory, Product,Category, ProductImage, AttributeValue, Cart, CartItem

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['url', 'alt_text']

class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name')

    class Meta:
        model = AttributeValue
        fields = ['attribute_name', 'value']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    attributes = AttributeValueSerializer(source='inventory__attributes', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'slug', 'category', 'images', 'attributes', 'is_active']



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'is_active']

class InventorySerializer(serializers.ModelSerializer):
    attributes = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'sku', 'price', 'attributes', 'is_active']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'inventory', 'quantity', 'is_active']

    

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'total_amount', 'is_active', 'cart_items']


