from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from products.models import Product
from .models import Cart

User = get_user_model()

class CartTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.product = Product.objects.create(name="Test Product", price=100.00, stock=10)
        self.client.login(username="testuser", password="testpass")

    def test_add_to_cart(self):
        response = self.client.post("/cart/add/", {"product": self.product.id, "quantity": 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.get(user=self.user).items.count(), 1)
