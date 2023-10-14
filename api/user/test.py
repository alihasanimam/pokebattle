from django.urls import reverse
from user.models import User
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.cache import cache

class UserTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('test', 'test@example.com', 'testtest')
        self.client.force_authenticate(user=self.user)

    def test_can_list_users(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_can_delete_user(self):
        url = reverse('user-list')
        response = self.client.delete('{}{}/'.format(url, self.user.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        count = User.objects.count()
        self.assertEqual(count, 0)