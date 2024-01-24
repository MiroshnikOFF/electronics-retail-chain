from django.db import models

from products.models import Product
from users.models import NULLABLE


class NetworkMember(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    email = models.EmailField(verbose_name='email')
    country = models.CharField(max_length=50, verbose_name='страна')
    city = models.CharField(max_length=50, verbose_name='город')
    street = models.CharField(max_length=50, verbose_name='улица')
    house_number = models.PositiveSmallIntegerField(verbose_name='номер дома')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')
    products = models.ManyToManyField(Product, verbose_name='продукты')
    status = models.CharField(editable=False, max_length=14, **NULLABLE, verbose_name='статус')

    class Meta:
        abstract = True


class Supplier(NetworkMember):
    factory_id = models.PositiveSmallIntegerField(editable=False, **NULLABLE, verbose_name='ID завода')
    retail_network_id = models.PositiveSmallIntegerField(editable=False, **NULLABLE, verbose_name='ID розничной сети')
    entrepreneur_id = models.PositiveSmallIntegerField(editable=False, **NULLABLE, verbose_name='ID ИП')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'поставщик'
        verbose_name_plural = 'поставщики'
        ordering = ('name',)
