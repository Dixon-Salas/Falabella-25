from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product
from rest_framework.views import APIView

class CartView(generics.RetrieveAPIView):
    """
    Retrieve the cart for the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=request.data['product'])
        quantity = request.data.get('quantity', 1)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        cart_item.save()

        return Response({'message': "Item added to cart"}, status=status.HTTP_201_CREATED)

class RemoveFromCartView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def delete(self,request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        product = Product.objects.get(id=request.data['product id'])
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        return Response({'message': "Item removed from cart"}, status=status.HTTP_200_OK)

class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        product = Product.objects.get(id=request.data['product'])
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity = request.data['quantity']
        cart_item.save()
        return Response({'message': 'Cart item updated successfully'}, status=status.HTTP_200_OK)

class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()  # Elimina todos los ítems del carrito
        return Response({'message': 'Cart cleared successfully'}, status=status.HTTP_200_OK)

class ConfirmOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el pedido
        total_price = sum(item.product.price * item.quantity for item in cart.items.all())
        order = Order.objects.create(user=request.user, total_price=total_price, status='pending')

        # Mover los ítems del carrito al pedido
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Vaciar el carrito
        cart.items.all().delete()

        return Response({'message': 'Order created successfully', 'order_id': order.id}, status=status.HTTP_201_CREATED)

