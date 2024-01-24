from django.contrib import admin

from members.models import Factory, RetailNetwork, Entrepreneur, Supplier
from members.management import MemberManager

manager = MemberManager()

distributor_or_seller_list_display = (
    'pk', 'name', 'email', 'country', 'city', 'street', 'house_number', 'created', 'supplier',
    'debt_to_supplier',
)


@admin.action(description='Очистить задолженность перед поставщиком')
def clear_debt(self, request, queryset):
    queryset.update(debt_to_supplier=0)


@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'country', 'city', 'street', 'house_number', 'created',)
    list_filter = ('city',)

    def save_model(self, request, obj, form, change):
        """
        При создании или обновлении завода сохраняет статус 'завод' и свой pk в этом объекте завода как поставщика
        """

        super().save_model(request, obj, form, change)
        supplier = Supplier.objects.get(pk=obj.pk)
        supplier.status = 'завод'
        supplier.factory_id = obj.pk
        supplier.save()


@admin.register(RetailNetwork)
class RetailNetworkAdmin(admin.ModelAdmin):
    list_display = distributor_or_seller_list_display
    list_filter = ('city',)
    actions = [clear_debt]

    def get_queryset(self, request):
        """
        При удалении розничных сетей используя admin action, удаляет все эти розничные сети из категории поставщиков
        """

        manager.delete_supplier(member_status='розничная сеть', request=request)
        queryset = super().get_queryset(request)
        return queryset


@admin.register(Entrepreneur)
class EntrepreneurAdmin(admin.ModelAdmin):
    list_display = distributor_or_seller_list_display
    list_filter = ('city',)
    actions = [clear_debt]

    def get_queryset(self, request):
        """
        При удалении предпринимателей используя admin action, удаляет всех этих предпринимателей
        из категории поставщиков
        """

        manager.delete_supplier(member_status='ИП', request=request)
        queryset = super().get_queryset(request)
        return queryset
