from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, Form
from django.utils.translation import gettext_lazy as _

from apps.user.models import User, Cart, Profile


class RegisterModelForm(ModelForm):
    confirm_password = CharField()

    class Meta:
        model = User
        fields = ("phone", "password", "confirm_password")

    def clean_password(self):
        password = self.cleaned_data["password"]
        if password:
            if len(password) < 8:
                msg = _('Password is short')
                self.add_error('password', msg)
        return password

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if User.objects.filter(phone=phone).exists():
            msg = _("This phone already registered")
            self.add_error("phone", msg)
        return phone

    def clean(self):
        if self.cleaned_data["password"] != self.cleaned_data["confirm_password"]:
            msg = _("Passwords do not match")
            self.add_error("confirm_password", msg)
        return self.cleaned_data

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        user = User.objects.get(
            phone=self.cleaned_data["phone"],
        )
        user.set_password(self.cleaned_data["password"])
        user.save()
        Cart.objects.create(user=user)
        Profile.objects.create(user=user)
        return user


class LoginForm(Form):
    phone = CharField(max_length=55)
    password = CharField()

    def clean(self):
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')
        msg = _('Phone number or password is incorrect!')
        if not User.objects.filter(phone=phone).exists() or not User.objects.filter(phone=phone).first().check_password(password):
            raise ValidationError(message=msg)
        return self.cleaned_data


class UpdateProfileForm(Form):
    first_name = CharField()
    last_name = CharField()
