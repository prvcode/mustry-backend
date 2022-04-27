from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects_user(**params)


class PublicUserApiTests(TestCase):

    """
    Test user API (public)
    """
    def setUp(self):
        self.client = APIClient

    def test_create_valid_user_success(self):
        """
        Test crateing user with valid payload
        """
        payload = {
            'email': 'test@prv.com',
            'password': 'test@8',
            'name': 'Test User'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """
        Test duplicate user
        """
        payload = {
            'email': 'test@prv.com',
            'password': 'test@8',
            'name': 'Test User'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
