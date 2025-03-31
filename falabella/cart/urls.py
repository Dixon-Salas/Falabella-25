from django.urls import path
from .views import CartView, AddToCartView, RemoveFromCartView, UpdateCartItemView, ClearCartView, ConfirmOrderView, OrderHistoryView, UpdateOrderStatusView

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("add/", AddToCartView.as_view(), name="add-to-cart"),
    path("remove/<int:product_id>/", RemoveFromCartView.as_view(), name="remove-from-cart"),
    path("update/", UpdateCartItemView.as_view(), name="update-cart-item"),  # Nueva ruta
    path("clear/", ClearCartView.as_view(), name="clear-cart"),
    path("confirm-order/", ConfirmOrderView.as_view(), name="confirm-order"),
    path("order-history/", OrderHistoryView.as_view(), name="order-history"),
    path("update-order-status/<int:order_id>/", UpdateOrderStatusView.as_view(), name="update-order-status"),
]
