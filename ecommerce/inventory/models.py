from django.db import models
from accounts.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    url = models.URLField()
    alt_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Product Images'

    def __str__(self):
        return self.url
    

class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Attributes'
    
    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='attribute_values')
    value = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Attribute Values'

    def __str__(self):
        return self.value



class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory')
    sku = models.CharField(max_length=100, unique=True)
    images = models.ManyToManyField(ProductImage, related_name='inventory')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    attributes = models.ManyToManyField(AttributeValue, related_name='inventory')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Inventory'

    def __str__(self):
        return self.product.name


class Stock(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='stock')
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Stock'

    def __str__(self):
        return f"{self.inventory.product.name} - {self.quantity} units" 


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Cart'

    def total_amount_price(self):
        self.total_amount = sum(item.inventory.price * item.quantity for item in self.cart_items.all())
        self.save()
        return self.total_amount

    def __str__(self):
        return f"{self.user.first_name}'s Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Cart Items'


    def __str__(self):
        return f"{self.cart.user.first_name}'s Cart Item"
    

# Can be developed when finalised on payment flow

# class ShippingAddress(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_address')
#     contact_details = models.CharField(max_length=15)
#     address = models.TextField()
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)
#     pincode = models.CharField(max_length=10)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)

#     class Meta:
#         verbose_name_plural = 'Shipping Address'

#     def __str__(self):
#         return f"{self.user.first_name}'s Shipping Address"


# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders')
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, related_name='orders')
#     contact_details = models.CharField(max_length=15)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)

#     class Meta:
#         verbose_name_plural = 'Orders'

#     def __str__(self):
#         return f"{self.user.first_name}'s Order"

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
#     inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='order_items')
#     quantity = models.IntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)

#     class Meta:
#         verbose_name_plural = 'Order Items'

#     def __str__(self):
#         return f"{self.order.user.first_name}'s Order Item"

