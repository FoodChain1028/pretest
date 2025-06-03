from django.db import models

class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    order_number = models.IntegerField()
    total_price = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
