import unittest
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.test import TestCase
import pytest
from rest_framework.test import APIClient
from rest_framework import status

class TokenTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = RefreshToken.for_user(self.user)

    def test_token_expiry(self):
        expected_expiry_time = datetime.now() + timedelta(minutes=5)  # Adjust based on your token settings
        self.assertLessEqual(self.token.access_token['exp'], expected_expiry_time.timestamp())

    def test_token_user_details(self):
        self.assertEqual(self.token.access_token['user_id'], self.user.id)
        self.assertEqual(self.token.access_token['username'], self.user.username)
        # Add more assertions for other user details as needed

if __name__ == '__main__':
    unittest.main()


@pytest.mark.django_db
class TestRegisterEndpoint:

    def setup_method(self, method):
        self.client = APIClient()

    def test_register_success_default_org(self):
        url = '/org/auth/register/'
        data = {
            'firstName': 'test',
            'lastName': 'b',
            'email': 'testb@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'accessToken' in response.data
        assert response.data['user']['firstName'] == 'test'
        # Add assertions for default organisation name and other expected data

    def test_login_success(self):
        url = '/org/auth/login/'
        data = {
            'email': 'testb@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'accessToken' in response.data
        assert response.data['user']['firstName'] == 'test'
        # Add more assertions for other expected data in login response

    def test_missing_required_fields(self):
        url = '/org/auth/register/'
        data = {
            'lastName': 'test',
            'email': 'testb@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        # Add assertions for specific error messages returned

    def test_duplicate_email_or_userID(self):
        # Implement test for attempting to register users with duplicate email/userID
        pass

