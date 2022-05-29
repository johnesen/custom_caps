from django.db import models

class Baner(models.Model):
    baner = models.FileField("baner", upload_to='baner/')
    baner_title = models.CharField("title", max_length=250)


    def __str__(self):
        return self.baner_title

    class Meta:
        verbose_name = "Банер"
        verbose_name_plural = "Банеры"

