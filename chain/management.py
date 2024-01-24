from members import models as member_model
from chain.models import Supplier
from members.models import RetailNetwork, Entrepreneur


class SupplierManager:

    @classmethod
    def create_member(cls, validated_data: dict) -> object:
        """ Создает участника сети на основе поставщика """

        status = validated_data.get('status')
        products = validated_data.pop('products', [])
        supplier_pk = validated_data.pop('supplier_pk', None)
        if status == 'завод':
            factory = member_model.Factory.objects.create(**validated_data)
            factory.products.set(products)
            return factory
        elif status == 'розничная сеть':
            retail_network = member_model.RetailNetwork.objects.create(**validated_data)
            retail_network.products.set(products)
            if supplier_pk:
                retail_network.supplier = Supplier.objects.get(pk=supplier_pk)
                retail_network.save()
            return Supplier.objects.get(retail_network_id=retail_network.pk)
        else:
            entrepreneur = member_model.Entrepreneur.objects.create(**validated_data)
            entrepreneur.products.set(products)
            if supplier_pk:
                entrepreneur.supplier = Supplier.objects.get(pk=supplier_pk)
                entrepreneur.save()
            return Supplier.objects.get(entrepreneur_id=entrepreneur.pk)

    @classmethod
    def get_member(cls, supplier) -> object:
        if supplier.status == 'розничная сеть':
            return RetailNetwork.objects.get(pk=supplier.retail_network_id)
        elif supplier.status == 'ИП':
            return Entrepreneur.objects.get(pk=supplier.entrepreneur_id)

    @classmethod
    def update_member(cls, instance, validated_data, products) -> None:
        """ Обновляет участника сети созданного на основе поставщика данными поставщика """

        if instance.status == 'розничная сеть':
            member_model.RetailNetwork.objects.filter(pk=instance.retail_network_id).update(**validated_data)
            retail_network = member_model.RetailNetwork.objects.get(pk=instance.retail_network_id)
            retail_network.products.set(products)
        elif instance.status == 'ИП':
            member_model.Entrepreneur.objects.filter(pk=instance.entrepreneur_id).update(**validated_data)
            entrepreneur = member_model.Entrepreneur.objects.get(pk=instance.entrepreneur_id)
            entrepreneur.products.set(products)

    @classmethod
    def delete_member(cls, supplier) -> None:
        """ Удаляет участника сети созданного на основе поставщика """

        if supplier.status == 'розничная сеть':
            RetailNetwork.objects.filter(pk=supplier.retail_network_id).delete()
        elif supplier.status == 'ИП':
            Entrepreneur.objects.filter(pk=supplier.entrepreneur_id).delete()
