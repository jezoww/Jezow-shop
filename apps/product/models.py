from django.db.models import *
from django.utils.text import slugify

from apps.product.choices import ProductSizeChoice, ProductGenderChoice


class BaseSlug(Model):
    class Meta:
        abstract = True

    name = CharField(max_length=255)
    slug = SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = self.slug + "1"
        return super().save(*args, **kwargs)


class Category(BaseSlug):
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(BaseSlug):
    price = PositiveIntegerField()
    description = TextField()
    category = ForeignKey(Category, on_delete=CASCADE, related_name='products')
    sold = IntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
    gender = CharField(max_length=25, choices=ProductGenderChoice.choices)

    def __str__(self):
        return self.name


class ProductImage(Model):
    image = ImageField(upload_to='product/')
    product = ForeignKey(Product, on_delete=CASCADE, related_name='images')


class AboutProduct(Model):
    product = ForeignKey(Product, on_delete=CASCADE, related_name='about_product')
    size = CharField(max_length=10, choices=ProductSizeChoice.choices, null=True, blank=True)
    quantity = IntegerField(default=1)
