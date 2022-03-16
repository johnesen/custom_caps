from django.db import models

class CapsInDigit(models.Model):
    saled = models.PositiveBigIntegerField("saled caps")
    year_in_market = models.PositiveIntegerField("yeears")
    clients = models.PositiveBigIntegerField("clients")
    
    class Meta:
        verbose_name = "Кепки в цифрах"
        verbose_name_plural = "Кепки в цифрах"
