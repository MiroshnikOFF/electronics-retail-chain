from rest_framework import serializers

from products.models import Product
from chain.models import Supplier
from members.models import RetailNetwork, Entrepreneur
from chain.management import SupplierManager
from chain.validators import StatusCreateValidator, status_update_validator, FactoryValidator, \
    debt_to_supplier_update_validator, SupplierAddValidator, DebtToSupplierValidator

manager = SupplierManager()


class SupplierSerializer(serializers.ModelSerializer):
    status = serializers.CharField(max_length=14, required=True)
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    supplier_pk = serializers.IntegerField(required=False)
    supplier = serializers.SerializerMethodField()
    debt_to_supplier = serializers.FloatField(required=False)
    debt = serializers.SerializerMethodField()

    class Meta:
        model = Supplier
        fields = (
            'id', 'status', 'name', 'email', 'products', 'country', 'city', 'street', 'house_number', 'created',
            'supplier_pk', 'supplier', 'debt_to_supplier', 'debt',
        )
        validators = (
            StatusCreateValidator(status_list=['завод', 'розничная сеть', 'ИП']),
            FactoryValidator(),
            SupplierAddValidator(),
            DebtToSupplierValidator(),
        )

    def create(self, validated_data):
        """ При создании поставщика создает участника сети на основе этого поставщика """

        supplier = manager.create_member(validated_data)
        return supplier

    def update(self, instance, validated_data):
        """ Обновляет продукты поставщика и участника торговой сети созданного на основе этого поставщика """

        products = validated_data.pop('products', [])
        validated_data.pop('supplier_pk')
        status_update_validator(instance, validated_data)
        debt_to_supplier_update_validator(instance, validated_data)

        instance = super().update(instance, validated_data)
        instance.products.set(products)
        manager.update_member(instance, validated_data, products)
        return instance

    @classmethod
    def get_supplier(cls, instance):
        """
        Получает pk поставщика из данных участника сети созданного на основе этого поставщика
        для заполнения поля supplier
        """

        if instance.status == 'розничная сеть':
            retail_network = RetailNetwork.objects.get(pk=instance.retail_network_id)
            if retail_network.supplier:
                return retail_network.supplier.pk
        elif instance.status == 'ИП':
            entrepreneur = Entrepreneur.objects.get(pk=instance.entrepreneur_id)
            if entrepreneur.supplier:
                return entrepreneur.supplier.pk

    @classmethod
    def get_debt(cls, instance):
        """
        Получает задолженность перед поставщиком из данных участника сети созданного на основе этого поставщика
        для заполнения поля debt
        """

        if instance.status == 'розничная сеть':
            retail_network = RetailNetwork.objects.get(pk=instance.retail_network_id)
            if retail_network.debt_to_supplier:
                return retail_network.debt_to_supplier
        elif instance.status == 'ИП':
            entrepreneur = Entrepreneur.objects.get(pk=instance.entrepreneur_id)
            if entrepreneur.debt_to_supplier:
                return entrepreneur.debt_to_supplier
