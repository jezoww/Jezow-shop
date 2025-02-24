from django.contrib import admin
from django.contrib.admin import StackedInline
from modeltranslation.admin import TranslationAdmin

from apps.product.models import Product, ProductImage, AboutProduct


class ProductImagesInline(StackedInline):
    model = ProductImage
    extra = 3


class AboutProductInline(StackedInline):
    model = AboutProduct
    extra = 3


class ProductAdmin(TranslationAdmin):
    inlines = [ProductImagesInline, AboutProductInline]
    exclude = 'slug',

    class Media:
        js = (
            "http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
