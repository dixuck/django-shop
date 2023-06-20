from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model

from .models import Product
from utils.utils import get_tokens_for_user

User = get_user_model()

class ProductTestCase(TestCase):

    def setUp(self) -> None:

        self.client = APIClient()

        user = User.objects.create(
            username='testuser',
            password='testpass',
            email='test@test.com',
            is_active=True,
        )

        admin = User.objects.create(
            username='testadmin',
            password='testpass',
            email='admin@test.com',
            is_staff=True,
            is_active=True,
        )

        self.URL = reverse('product-list')
        self.DETAIL_URL = reverse('product-detail', ['test-product'])
        Product.objects.create(title='test-product')
        self.user_token = get_tokens_for_user(user)
        self.admin_token = get_tokens_for_user(admin)

    def test_get_products(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)
        