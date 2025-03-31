from django.urls import path
from .views import CartView, AddToCartView, RemoveFromCartView, UpdateCartItemView, ClearCartView, ConfirmOrderView

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("add/", AddToCartView.as_view(), name="add-to-cart"),
    path("remove/<int:product_id>/", RemoveFromCartView.as_view(), name="remove-from-cart"),
    path("update/", UpdateCartItemView.as_view(), name="update-cart-item"),  # Nueva ruta
    path("clear/", ClearCartView.as_view(), name="clear-cart"),
    path("confirm-order/", ConfirmOrderView.as_view(), name="confirm-order"),
]
