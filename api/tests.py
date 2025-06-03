from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Order

ACCEPTED_TOKEN = ('omni_pretest_token')
ENDPOINT = 'http://127.0.0.1:8008/'

class OrderTestCase(APITestCase):
    def setUp(self):
        self.url = f"{ENDPOINT}api/import-order/"
        self.data = {
            'token': 'omni_pretest_token',
            'order_number': 123,
            'total_price': 100,
        }
    # make sure the code coverage is at least 90%
    # 1. test_no_token
    # 2. test_invalid_token
    # 3. test_no_order_number
    # 4. test_order_number_invalid_type
    # 5. test_no_total_price
    # 6. test_total_price_invalid_type
    # 7. test_create_order

    def test_no_token(self):
        self.setUp()
        self.data.pop('token')
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.json()['message'], 'Token is required')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)

    def test_invalid_token(self):
        self.setUp()
        self.data['token'] = 'invalid_token'
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.json()['message'], 'Invalid Access Token')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)

    def test_no_order_number(self):
        self.setUp()
        self.data.pop('order_number')
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['message'], 'Order number is required')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)
    
    def test_order_number_invalid_type(self):
        self.setUp()
        self.data['order_number'] = 'invalid_order_number'
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['message'], 'Order number must be an integer')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)
    
    def test_no_total_price(self):
        self.setUp()
        self.data.pop('total_price')
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['message'], 'Total price is required')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)

    def test_total_price_invalid_type(self):
        self.setUp()
        self.data['total_price'] = 'invalid_total_price'
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['message'], 'Total price must be an integer')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)

    def test_create_order(self):
        self.setUp()
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
