from abc import ABC, abstractmethod
from typing import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.products.filters import ProductFilters
from core.apps.products.entities.products import Product
from core.apps.products.models.products import Product as ProductModel

class BaseProductService(ABC):
    

    @abstractmethod
    def get_product_list(self, filters: ProductFilters) -> Iterable[Product]:
        ...


    @abstractmethod
    def get_product_count(self, filters: ProductFilters, pagination: PaginationIn) -> int:
        ...
    
# TODO: закинуть фильтры в слой сервисов, чтобы избежать нарушения инверсии зависимостей
class ORMProductService(BaseProductService):

    def _build_product_query(self, filters: ProductFilters) -> Q:

        query = Q(is_visible=True)

        if filters.search is not None:
            query &= (Q(title__icontains=filters.search) | Q(description__icontains=filters.search))

        return query

    def get_product_list(
            self,
            filters: ProductFilters,
            pagination: PaginationIn
        ) -> Iterable[Product]:

        query = self._build_product_query(filters)
        qs = ProductModel.objects.filter(query)
        return [product_dto.to_entity() for product_dto in qs][pagination.offset: pagination.offset + pagination.limit]

    def get_product_count(self, filters: ProductFilters) -> int:
        
        query = self._build_product_query(filters)
        procuct_count = ProductModel.objects.filter(query).count()
        return procuct_count