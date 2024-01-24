from rest_framework.serializers import ValidationError

from chain.management import SupplierManager
from chain.models import Supplier


manager = SupplierManager()


class StatusCreateValidator:

    def __init__(self, status_list: list) -> None:
        self.status_list = status_list

    def __call__(self, value):
        if value.get('status') not in self.status_list:
            raise ValidationError(
                "Неверный статус поставщика! Корректные варианты статуса: 'завод', 'розничная сеть', 'ИП'"
            )


class FactoryValidator:

    def __call__(self, value):
        status = value.get('status')
        if status == 'завод' and 'supplier_pk' in value:
            raise ValidationError("У завода не может быть поставщика!")
        if status == 'завод' and 'debt_to_supplier' in value:
            raise ValidationError("У завода не может быть задолженности перед поставщиком!")


class SupplierAddValidator:

    def __call__(self, value):
        supplier_pk = value.get('supplier_pk')
        if supplier_pk:
            if not Supplier.objects.filter(pk=supplier_pk).exists():
                raise ValidationError("Поставщика с таким ID не существует!")


class DebtToSupplierValidator:

    def __call__(self, value):
        if not value.get('supplier_pk') and value.get('debt_to_supplier'):
            raise ValidationError("Невозможно установить задолженность перед поставщиком при отсутствии поставщика!")


def status_update_validator(instance, validated_data):
    if instance.status != validated_data.get('status'):
        raise ValidationError(f"Недопустимо менять статус поставщика! Этот поставщик {instance.status}")


def debt_to_supplier_update_validator(instance, validated_data):
    member = manager.get_member(instance)
    if member:
        if member.debt_to_supplier and 'debt_to_supplier' in validated_data:
            raise ValidationError(
                "У участника торговой сети есть задолженность перед поставщиком! "
                "Запрещено обновлять задолженность при ее наличии!"
            )
