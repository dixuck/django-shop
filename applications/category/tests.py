from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model

from .models import Category
from utils.utils import get_tokens_for_user

User = get_user_model()

class CategoryTestCase(TestCase):

    def setUp(self) -> None:

        self.client = APIClient()
        self.URL = reverse('category-list')

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

        self.DETAIL_URL = reverse('category-detail', ['test-category'])
        Category.objects.create(title='test-category')
        self.user_token = get_tokens_for_user(user)
        self.admin_token = get_tokens_for_user(admin)

    def test_get_categories(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)

    def test_create_category_as_anon(self):
        response = self.client.post(self.URL, {'title': 'ыаыаы'})
        self.assertEqual(response.status_code, 401)

    def test_create_category_as_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token['access'])
        response = self.client.post(self.URL, {'title': 'ЫЫЫ'})
        self.assertEqual(response.status_code, 403)

    def test_create_category_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token['access'])
        response = self.client.post(self.URL, {'title': 'ЫЫЫ'})
        self.assertEqual(response.status_code, 201)

    def test_admin_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token['access'])
        response = self.client.patch(self.DETAIL_URL, {'title': 'new_title'})
        self.assertEqual(response.status_code, 200)


# TODO: написать тесты для продуктов