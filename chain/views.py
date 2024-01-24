from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from chain.management import SupplierManager
from chain.models import Supplier
from chain.serializers import SupplierSerializer
from chain.paginators import SupplierPaginator

manager = SupplierManager()


class SupplierCreateAPIView(generics.CreateAPIView):
    serializer_class = SupplierSerializer
    permission_classes = (IsAuthenticated,)


class SupplierListAPIView(generics.ListAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    pagination_class = SupplierPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('country',)
    permission_classes = (IsAuthenticated,)


class SupplierRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = (IsAuthenticated,)


class SupplierUpdateAPIView(generics.UpdateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = (IsAuthenticated,)


class SupplierDestroyAPIView(generics.DestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        """ При удалении поставщика удаляет созданного на его основе участника сети """
        manager.delete_member(instance)
        super().perform_destroy(instance)
