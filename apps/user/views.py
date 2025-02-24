from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, FormView, TemplateView, UpdateView

from apps.product.models import Product
from apps.user.forms import RegisterModelForm, LoginForm, UpdateProfileForm
from apps.user.models import AboutCart, User, Profile, Address, Order, AboutOrder
from django.utils.translation import gettext_lazy as _


class IndexListView(ListView):
    template_name = 'index.html'

    def get_queryset(self):
        return Product.objects.prefetch_related('images').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        products = self.get_queryset()
        new_arrivals = products.order_by("-created_at")[:6]
        if self.request.user.is_authenticated:
            cart_count = AboutCart.objects.filter(cart=self.request.user.cart).count()
        else:
            cart_count = 0

        context['cart_count'] = cart_count
        context['best_products'] = products.order_by('?')[:3]
        context['more_deals'] = products.order_by('-sold')[:3]
        context['new_arrivals_f'] = new_arrivals[:3]
        context['new_arrivals_s'] = new_arrivals[3:]
        context['recommend'] = products.order_by('sold')[:5]

        return context


class RegisterCreateView(CreateView):
    model = User
    form_class = RegisterModelForm
    success_url = reverse_lazy('index')
    template_name = 'user/register.html'

    def form_valid(self, form):
        msg = _("Successfully registered!")
        messages.success(self.request, msg)
        return super().form_valid(form)

    def form_invalid(self, form):
        for e in form.errors.values():
            messages.error(self.request, e)
        return super().form_invalid(form)


class LoginFormView(FormView):
    template_name = 'user/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        phone = form.cleaned_data.get('phone')
        user = User.objects.get(phone=phone)
        login(self.request, user)
        msg = _("Successfully logged in!")
        messages.success(self.request, msg)
        return super().form_valid(form)

    def form_invalid(self, form):
        for e in form.errors.values():
            messages.error(self.request, e)
        return super().form_invalid(form)


class AboutUsTemplateView(TemplateView):
    template_name = 'product/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart_count = AboutCart.objects.filter(cart=self.request.user.cart).count()
        else:
            cart_count = 0
        context['cart_count'] = cart_count
        return context


class CartListView(LoginRequiredMixin, ListView):
    template_name = 'user/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return AboutCart.objects.filter(cart=self.request.user.cart).prefetch_related('product__images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_queryset()
        cart_subtotal = sum(item.quantity * item.product.price for item in cart_items)
        cart_total = cart_subtotal
        context['cart_subtotal'] = intcomma(cart_subtotal)
        context['cart_total'] = intcomma(cart_total)

        return context


class ProfileTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile.html'


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        msg = _("Successfully logged out!")
        messages.success(request, msg)
        return redirect('index')


class ProfileFormView(LoginRequiredMixin, FormView):
    template_name = 'user/update-data.html'
    form_class = UpdateProfileForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        profile = self.request.user.profile
        data = form.cleaned_data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if first_name:
            profile.first_name = first_name
        if last_name:
            profile.last_name = last_name

        profile.save()
        return super().form_valid(form)


class ChangeAddressView(View):
    def post(self, request):
        if 'address_id' in request.POST:  # Updating an existing address
            address_id = request.POST.get('address_id')
            address = get_object_or_404(Address, id=address_id, user=request.user)
            new_address = request.POST.get(f'address_{address_id}')
            if new_address:
                address.address = new_address
                address.save()
        elif 'new_address' in request.POST:  # Adding a new address
            new_address = request.POST.get('new_address')
            if new_address:
                Address.objects.create(user=request.user, address=new_address)

        return redirect('profile')


class HistoryListView(LoginRequiredMixin, ListView):
    template_name = 'user/history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart_count = AboutCart.objects.filter(cart=self.request.user.cart).count()
        else:
            cart_count = 0
        context['cart_count'] = cart_count
        return context


class CreateOrderView(LoginRequiredMixin, View):
    def post(self, request):
        abouts = request.user.cart.about.all()
        if abouts:
            user = request.user
            address = request.POST.get('address')
            if not address or not user.addresses.exists():
                msg = _("Before ordering, please add your location.")
                messages.warning(request, msg)
                return redirect("profile")
            subtotal = 0
            for item in abouts:
                subtotal += item.get_subtotal
            order = Order.objects.create(user=user, shipping_price=15000, location=address, subtotal=subtotal)
            for about in abouts:
                product = about.product
                AboutOrder.objects.create(product=product,
                                          quantity=about.quantity,
                                          order=order,
                                          size=about.size)
                about.delete()
            msg = _("Ordered!")
            messages.success(self.request, msg)
            return redirect('history')
        else:
            msg = _("You do not have any products.")
            messages.warning(request, msg)
            return redirect("cart")


class OrderView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        items = order.about.all()
        data = {
            "items": [
                {
                    "image_url": item.product.images.first().image.url,
                    "product_name": item.product.name,
                    "size": item.size,
                    "quantity": item.quantity,
                    "price": item.get_subtotal,
                }
                for item in items
            ]
        }
        return JsonResponse(data)
