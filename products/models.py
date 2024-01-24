from django.db import models

from users.models import NULLABLE


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    model = models.CharField(**NULLABLE, max_length=150, verbose_name='модель')
    launch_date = models.DateField(**NULLABLE, verbose_name='дата выхода на рынок')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('name',)
