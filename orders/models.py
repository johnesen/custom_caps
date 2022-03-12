from django.db import models
from django.contrib.auth.models import User
from caps.models import Caps, Basket

class Status(models.Model):
    """модель статуса заказа"""
    status = models.CharField("Статус заказа", max_length=30)

    def __str__(self):
        return self.status  
    class Meta:
        verbose_name = "Статус заказа"
        verbose_name_plural = "Статус заказов"
        
class Order(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='order')
    order_date = models.DateField("Дата заказа", auto_now_add=True)

    def __str__(self):
        return f'{self.basket}'

    class Meta:
        verbose_name = "Товар заказа"
        verbose_name_plural = "Товары заказов"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name="Заказ", on_delete=models.CASCADE)
    order_code = models.CharField("Код заказа", max_length=100)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name="Статус")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    send_date = models.DateField()



    def __str__(self):
        return f'{self.order}'

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"