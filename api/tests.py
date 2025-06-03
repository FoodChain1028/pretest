from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Order, Product
from django.urls import reverse

ACCEPTED_TOKEN = ('omni_pretest_token')
ENDPOINT = 'http://127.0.0.1:8008/'

class OrderTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )

        self.product1 = Product.objects.create(
            name='Test Product 1',
            description='Test Description 1',
            price=49
        )
        self.product2 = Product.objects.create(
            name='Test Product 2',
            description='Test Description 2',
            price=51
        )

        self.url = f"{ENDPOINT}api/import-order/"
        self.data = {
            'token': 'omni_pretest_token',
            'user_id': self.user.id,
            'order_number': 123,
            'total_price': 100,
            'product_ids': [self.product1.id, self.product2.id]
        }

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
        self.assertEqual(res.json()['message'], 'Order number must be an number')

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
        self.assertEqual(res.json()['message'], 'Total price must be an number')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)

    def test_invalid_product_ids(self):
        self.data['product_ids'][0] = 99999
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['message'], 'One or more products not found')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)

    def test_missing_products(self):
        self.data['product_ids'].clear()
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['message'], 'At least one product is required')

        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)
    
    def test_incorrect_total_price(self):
        self.data['total_price'] = 101
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['message'], f"Total price is incorrect. Calculated sum {self.product1.price + self.product2.price} does not match provided total price {self.data['total_price']}.")
        
        # database
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Order.objects.first(), None)

    def test_successful_order_import(self):
        res = self.client.post(self.url, self.data, format='json')
        # response
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['message'], 'Order imported successfully')
        self.assertEqual(res.json()['order_id'], 1)
        self.assertEqual(res.json()['order_number'], 123)
        self.assertEqual(res.json()['total_price'], 100)
               
        # Verify products in response
        res_data = res.json()
        self.assertIn('products', res_data)
        self.assertEqual(len(res_data['products']), 2)
        
        # Verify first product details
        product1_data = res_data['products'][0]
        self.assertEqual(product1_data['id'], self.product1.id)
        self.assertEqual(product1_data['name'], self.product1.name)
        self.assertEqual(product1_data['description'], self.product1.description)
        self.assertEqual(product1_data['price'], self.product1.price)
        
        # Verify second product details
        product2_data = res_data['products'][1]
        self.assertEqual(product2_data['id'], self.product2.id)
        self.assertEqual(product2_data['name'], self.product2.name)
        self.assertEqual(product2_data['description'], self.product2.description)
        self.assertEqual(product2_data['price'], self.product2.price)

        # database
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().order_number, 123)
        self.assertEqual(Order.objects.first().total_price, 100)
        self.assertEqual(Order.objects.first().products.count(), 2)
        self.assertEqual(Order.objects.first().products.first().id, self.product1.id)
        self.assertEqual(Order.objects.first().products.last().id, self.product2.id)
 