from django.db import models
from users.models import User
from caps.models import Caps
from .utils import OrderStatus

        
class Order(models.Model):
    item = models.ForeignKey(Caps, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField("Статус заказа", max_length=250, choices=OrderStatus.choices(), default=OrderStatus.PEPARING)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Заказчик", related_name='orders')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=250)
    send_date = models.DateField(null=True, blank=True)
    order_date = models.DateField("Дата заказа", auto_now_add=True)


    def __str__(self):
        return f'{self.item} - {self.user}'