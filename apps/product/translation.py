from modeltranslation.translator import register, TranslationOptions

from apps.product.models import Product, Category


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', )


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )
