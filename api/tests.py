from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Order

ACCEPTED_TOKEN = ('omni_pretest_token')
ENDPOINT = 'http://127.0.0.1:8008/'

class OrderTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )

        self.url = f"{ENDPOINT}api/import-order/"
        self.data = {
            'token': 'omni_pretest_token',
            'user_id': self.user.id,
            'order_number': 123,
            'total_price': 100,
        }
    
    # def tearDown(self):
    #     User.objects.all().delete()
    #     Order.objects.all().delete()
    # make sure the code coverage is at least 90%
    # 1. test_no_token
    # 2. test_invalid_token
    # 3. test_no_user_id
    # 4. test_invalid_user_id
    # 5. test_no_order_number
    # 6. test_order_number_invalid_type
    # 7. test_no_total_price
    # 8. test_total_price_invalid_type
    # 9. test_create_order

    def test_no_token(self):
        self.data.pop('token')
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.json()['message'], 'Token is required')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)

    def test_invalid_token(self):
        self.data['token'] = 'invalid_token'
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.json()['message'], 'Invalid Access Token')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)

    def test_no_user_id(self):
        self.data.pop('user_id')
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['message'], 'User ID is required')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)

    def test_user_id_invalid_type(self):
        self.data['user_id'] = 'invalid_user_id'
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['message'], 'User ID must be an number')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)

    def test_invalid_user_id(self):
        self.data['user_id'] = '131313'
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['message'], 'Invalid user ID')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)

    def test_no_order_number(self):
        self.data.pop('order_number')
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['message'], 'Order number is required')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)
    
    def test_order_number_invalid_type(self):
        self.data['order_number'] = 'invalid_order_number'
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['message'], 'Order number must be an integer')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)
    
    def test_no_total_price(self):
        self.data.pop('total_price')
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['message'], 'Total price is required')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)

    def test_total_price_invalid_type(self):
        self.data['total_price'] = 'invalid_total_price'
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['message'], 'Total price must be an integer')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)

    def test_create_order(self):
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['message'], 'Order imported successfully')
        self.assertEqual(res.json()['order_id'], 1)
        self.assertEqual(res.json()['order_number'], 123)
        self.assertEqual(res.json()['total_price'], 100)
        
        # database
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().order_number, 123)
        self.assertEqual(Order.objects.first().total_price, 100)
