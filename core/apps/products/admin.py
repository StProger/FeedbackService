from django.contrib import admin

from djangoql.admin import DjangoQLSearchMixin

from core.apps.products.models.products import Product


@admin.register(Product)
class ProductAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    
    list_display = ('id', 'title', 'description', 'created_at', 'updated_at', 'is_visible')