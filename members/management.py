from members import models as member_model
from chain.models import Supplier


class MemberManager:

    @classmethod
    def set_status(cls, candidate) -> str:
        """ Устанавливает статус участника сети в зависимости от его модели """

        if isinstance(candidate, member_model.RetailNetwork):
            return 'розничная сеть'
        else:
            return 'ИП'

    @classmethod
    def check_supplier_availability(cls, pk: int) -> bool:
        """ Проверяет наличие участника сети в категории поставщиков """

        if Supplier.objects.filter(retail_network_id=pk).exists():
            return True
        return Supplier.objects.filter(entrepreneur_id=pk).exists()

    @classmethod
    def get_supplier(cls, pk: int) -> object:
        """ Получает участника сети из категории поставщиков """

        if Supplier.objects.filter(retail_network_id=pk).exists():
            return Supplier.objects.get(retail_network_id=pk)
        return Supplier.objects.get(entrepreneur_id=pk)

    @classmethod
    def get_members_list_pk(cls, request) -> list:
        """
        Получает список pk участников сети из request метода get_queryset класса ModelAdmin
        при использовании admin action
        """

        if request.method == 'POST':
            if request.POST.get('action') == 'delete_selected' and request.POST.get('post'):
                return request.POST.getlist('_selected_action')

    @classmethod
    def create_supplier(cls, candidate) -> None:
        """ Создает поставщика на основе данных участника сети, после чего участник может быть поставщиком """

        if not cls.check_supplier_availability(candidate.pk):
            if isinstance(candidate, member_model.RetailNetwork):
                retail_network_pk = candidate.pk
                entrepreneur_pk = None
            else:
                retail_network_pk = None
                entrepreneur_pk = candidate.pk
            Supplier.objects.create(
                name=candidate.name,
                status=candidate.status,
                email=candidate.email,
                country=candidate.country,
                city=candidate.city,
                street=candidate.street,
                house_number=candidate.house_number,
                created=candidate.created,
                retail_network_id=retail_network_pk,
                entrepreneur_id=entrepreneur_pk
            )

    @classmethod
    def set_supplier_products(cls, member) -> None:
        """ Устанавливает продукты участника сети созданному на его основе поставщику """

        if member.status == 'розничная сеть':
            supplier = Supplier.objects.get(retail_network_id=member.pk)
        else:
            supplier = Supplier.objects.get(entrepreneur_id=member.pk)
        supplier.products.set(member.products.all())

    @classmethod
    def update_supplier(cls, candidate) -> None:
        """ Обновляет данными участника сети созданного на его основе поставщика """

        supplier = cls.get_supplier(candidate.pk)

        supplier.name = candidate.name
        supplier.email = candidate.email
        supplier.country = candidate.country
        supplier.city = candidate.city
        supplier.street = candidate.street
        supplier.house_number = candidate.house_number
        supplier.products.set(candidate.products.all())

        supplier.save()

    @classmethod
    def delete_supplier(cls, member_status: str, member_pk=None, request=None) -> None:
        """ Удаляет участника сети из категории поставщиков при его удалении """

        # при прямом удалении посредством метода delete модели
        if member_pk:
            if member_status == 'розничная сеть':
                Supplier.objects.filter(retail_network_id=member_pk).delete()
            else:
                Supplier.objects.filter(entrepreneur_id=member_pk).delete()

        # при удалении используя admin action
        else:
            if cls.get_members_list_pk(request):
                member_list_pk = cls.get_members_list_pk(request)
                if member_status == 'розничная сеть':
                    Supplier.objects.filter(retail_network_id__in=member_list_pk).delete()
                else:
                    Supplier.objects.filter(entrepreneur_id__in=member_list_pk).delete()
