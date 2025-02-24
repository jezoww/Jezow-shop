from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import *
from phonenumber_field.modelfields import PhoneNumberField

from apps.product.choices import ProductSizeChoice
from apps.product.models import Product


class CustomUserManager(UserManager):
    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError("The given phone must be set")
        user = self.model(phone=phone, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    phone = PhoneNumberField(region='UZ', unique=True)
    email = EmailField(null=True, blank=True)
    username = None
    first_name = None
    last_name = None

    objects = CustomUserManager()
    USERNAME_FIELD = 'phone'

    def __str__(self):
        return str(self.phone)


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='profile')
    first_name = CharField(max_length=255, null=True, blank=True)
    last_name = CharField(max_length=255, null=True, blank=True)


class Likes(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='likes')
    product = ForeignKey(Product, on_delete=CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'product')


class Cart(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='cart')


class AboutCart(Model):
    cart = ForeignKey(Cart, on_delete=CASCADE, related_name='about')
    product = ForeignKey(Product, on_delete=CASCADE, related_name='about')
    size = CharField(max_length=10, choices=ProductSizeChoice.choices, null=True, blank=True)
    quantity = PositiveSmallIntegerField()

    @property
    def get_subtotal(self):
        return self.product.price * self.quantity


class Order(Model):
    class ORDERSTATUSCHOICE(TextChoices):
        in_process = "In process", "in process"
        canceled = "Canceled", "canceled"
        delivered = "Delivered", "delivered"
        delivering = "Delivering", 'delivering'

    user = ForeignKey(User, on_delete=CASCADE, related_name='orders')
    status = CharField(choices=ORDERSTATUSCHOICE.choices, max_length=100, default="in process")
    created_at = DateTimeField(auto_now_add=True)
    shipping_price = IntegerField()
    location = CharField(max_length=512)
    subtotal = BigIntegerField()


class AboutOrder(Model):
    order = ForeignKey(Order, on_delete=CASCADE, related_name='about')
    product = ForeignKey(Product, on_delete=CASCADE, related_name='about_order')
    quantity = PositiveSmallIntegerField()
    size = CharField(max_length=10, choices=ProductSizeChoice.choices, null=True, blank=True)

    @property
    def get_subtotal(self):
        return self.product.price * self.quantity


class Address(Model):
    address = CharField(max_length=512)
    user = ForeignKey(User, on_delete=CASCADE, related_name='addresses')
