from django.db import models
from django.dispatch import receiver

from chain.models import NetworkMember, Supplier
from products.models import Product
from users.models import NULLABLE
from members.management import MemberManager

manager = MemberManager()


class DistributorOrSeller(NetworkMember):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, **NULLABLE, verbose_name='поставщик')
    debt_to_supplier = models.FloatField(**NULLABLE, verbose_name='задолженность перед поставщиком')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """ При создании или изменении участника сети, удаляет или изменяет поставщика созданного на его основе """

        self.status = manager.set_status(self)
        if self.pk:
            manager.update_supplier(self)
        super().save(*args, **kwargs)
        manager.create_supplier(self)

    def delete(self, *args, **kwargs):
        """ При удалении участника сети, удаляет его из категории поставщиков """

        manager.delete_supplier(member_pk=self.pk, member_status=self.status)
        super().delete(*args, **kwargs)


class Factory(Supplier):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'завод'
        verbose_name_plural = 'заводы'
        ordering = ('name',)


class RetailNetwork(DistributorOrSeller):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'розничная сеть'
        verbose_name_plural = 'розничные сети'
        ordering = ('name',)


class Entrepreneur(DistributorOrSeller):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'индивидуальный предприниматель'
        verbose_name_plural = 'индивидуальные предприниматели'
        ordering = ('name',)


@receiver(models.signals.m2m_changed, sender=RetailNetwork.products.through)
@receiver(models.signals.m2m_changed, sender=Entrepreneur.products.through)
def create_supplier_relation_with_products(sender, instance, action, **kwargs):
    """
    Сигнал срабатывающий сразу после создания участника сети и создания связи m2m с продуктами.
    Необходим для создания связи m2m с поставщиком созданном на основе участника сети, так как во время создания
    участника и поставщика на его основе связь с продуктами еще отсутствует
    """

    if action == 'post_add':
        manager.set_supplier_products(instance)
    elif action == 'post_remove':
        manager.set_supplier_products(instance)
