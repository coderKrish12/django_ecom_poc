from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import Product,Cart,CartItem,Inventory,Stock
from .serializers import ProductSerializer,CartSerializer,CartItemSerializer,InventorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

# Create your views here.

class ProductView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name','slug','description']
    ordering_fields = ['name', 'price']
    filterset_fields = ['category','is_active']

    def retrieve(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        product_data = ProductSerializer(product).data  
        inventory_data = InventorySerializer(product.inventory.all(), many=True).data 
        return Response({"product": product_data, "inventory": inventory_data}) 


class CartView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        """Retrieve the cart for the authenticated user, or create one if it doesn't exist."""
        cart, created = Cart.objects.get_or_create(user=user)
        if created:
            cart.total_amount = 0  # Initialize total_amount if cart is newly created
            cart.save()
        return cart

    def list(self, request):
        """Retrieve the current user's cart."""
        cart = self.get_cart(request.user)
        
        total_amount = 0
        for cart_item in cart.cart_items.all():
            total_amount += cart_item.quantity * cart_item.inventory.price

        cart.total_amount = total_amount
        cart.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def create(self, request):
        """Add an item to the cart."""
        cart = self.get_cart(request.user)
        inventory_id = request.data.get('inventory_id')
        quantity = request.data.get('quantity')

        if not inventory_id:
            return Response({"error": "Inventory ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the inventory item
        inventory = get_object_or_404(Inventory, id=inventory_id)

        # Assuming Inventory has a related Stock model that holds the quantity
        stock = get_object_or_404(Stock, inventory=inventory)

        # Check if the item is already in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, inventory=inventory)

        # Check if there is enough stock in inventory
        if stock.quantity < quantity + cart_item.quantity:
            return Response({"error": "Not enough stock available."}, status=status.HTTP_400_BAD_REQUEST)


        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()
        cart.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Update the quantity of a cart item."""
        cart = self.get_cart(request.user)
        cart_item = get_object_or_404(CartItem, id=pk, cart=cart)

        quantity = request.data.get('quantity', 0)
        if quantity <= 0:
            cart_item.delete()
            return Response({"message": "Item removed from the cart."}, status=status.HTTP_204_NO_CONTENT)

        cart_item.quantity = quantity
        cart_item.save()
        cart.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Remove an item from the cart."""
        cart = self.get_cart(request.user)
        cart_item = get_object_or_404(CartItem, id=pk, cart=cart)
        cart_item.delete()
        cart.save()

        return Response({"message": "Item removed from the cart."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='clear')
    def clear_cart(self, request):
        """Clear all items from the cart."""
        cart = self.get_cart(request.user)
        cart.cart_items.all().delete()
        cart.total_amount = 0
        cart.save()
        return Response({"message": "Cart cleared."}, status=status.HTTP_204_NO_CONTENT)