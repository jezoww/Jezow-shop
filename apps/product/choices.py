from django.db.models import TextChoices


class ProductSizeChoice(TextChoices):
    XS = ('XS', 'XS')
    S = ('S', 'S')
    M = ('M', 'M')
    L = ('L', 'L')
    XL = ('XL', 'XL')
    XXL = ('XXL', 'XXL')
    XXXL = ('XXXL', 'XXXL')

class ProductGenderChoice(TextChoices):
    male = ('male', "Male")
    female = ('female', "Female")
    unisex = ('unisex', "Unisex")