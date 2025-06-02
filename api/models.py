from django.db import models

class Order(models.Model):
    order_number = models.IntegerField()
    total_price = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
