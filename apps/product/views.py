import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DetailView, ListView

from apps.product.models import Product
from apps.user.models import AboutCart


class ProductDetailView(DetailView):
    template_name = 'product/detail.html'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Product.objects.prefetch_related('images').select_related('category').filter(slug=self.kwargs.get('slug'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart_count = AboutCart.objects.filter(cart=self.request.user.cart).count()
        else:
            cart_count = 0

        product = self.get_object()
        products = (
            Product.objects.filter(category=product.category).prefetch_related('images')
            .exclude(id=product.id)
            .order_by("-id")[:5]
        )
        context['products'] = products
        context['cart_count'] = cart_count
        return context


class ShopMenListView(ListView):
    template_name = 'product/shop.html'
    context_object_name = 'products'
    paginate_by = 24

    def get_queryset(self):
        return Product.objects.filter(Q(gender='male') | Q(gender='unisex')).prefetch_related('images')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.request.user.is_authenticated:
            cart_count = AboutCart.objects.filter(cart=self.request.user.cart).count()
        else:
            cart_count = 0
        context['page'] = _("Men")
        context['cart_count'] = cart_count
        return context


class ShopWomenListView(ListView):
    template_name = 'product/shop.html'
    context_object_name = 'products'
    paginate_by = 24

    def get_queryset(self):
        return Product.objects.filter(Q(gender='female') | Q(gender='unisex')).prefetch_related('images')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.request.user.is_authenticated:
            cart_count = AboutCart.objects.filter(cart=self.request.user.cart).count()
        else:
            cart_count = 0
        context['page'] = _("Women")
        context['cart_count'] = cart_count
        return context


class NewArrivalsListView(ListView):
    template_name = 'product/shop.html'
    context_object_name = 'products'
    paginate_by = 24

    def get_queryset(self):
        return Product.objects.order_by('-created_at').prefetch_related('images')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.request.user.is_authenticated:
            cart_count = AboutCart.objects.filter(cart=self.request.user.cart).count()
        else:
            cart_count = 0
        context['page'] = _("New arrivals")
        context['cart_count'] = cart_count
        return context


class BestProductsListView(ListView):
    template_name = 'product/shop.html'
    context_object_name = 'products'
    paginate_by = 24

    def get_queryset(self):
        return Product.objects.order_by('-sold').prefetch_related('images')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.request.user.is_authenticated:
            cart_count = AboutCart.objects.filter(cart=self.request.user.cart).count()
        else:
            cart_count = 0
        context['page'] = _("Best products")
        context['cart_count'] = cart_count
        return context


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, slug):
        cart = request.user.cart
        product = Product.objects.get(slug=slug)
        size = request.GET.get('size')
        if AboutCart.objects.filter(cart=cart, product=product, size=size).exists():
            cart_item = AboutCart.objects.get(product=product, cart=cart, size=size)
            cart_item.quantity += 1
            cart_item.save()
            msg = _("Added!")
            messages.success(self.request, msg)
            return redirect('product-detail', slug=product.slug)
        AboutCart.objects.create(cart=cart, product=product, quantity=1, size=size)
        messages.success(self.request, "Added!")
        return redirect('product-detail', slug=product.slug)

    def post(self, request, slug):
        data = json.loads(request.body)
        product = Product.objects.get(slug=slug)
        quantity = data.get('quantity')
        size = data.get('size')
        cart = request.user.cart
        aboutcart = AboutCart.objects.get(cart=cart, product=product, size=size)
        if int(quantity) != 0:
            aboutcart.quantity = quantity
            aboutcart.save()
        else:
            aboutcart.delete()
        cart_items = AboutCart.objects.filter(cart=cart)
        cart_subtotal = sum(item.get_subtotal for item in cart_items)
        cart_total = cart_subtotal

        # Prepare response data
        response_data = {
            'cart_subtotal': intcomma(cart_subtotal),
            'cart_total': intcomma(cart_total),
            'cart_items': [
                {
                    'product_id': item.product.id,
                    'quantity': item.quantity,
                } for item in cart_items
            ]
        }

        return JsonResponse(response_data)


class ProductDeleteView(View):
    def get(self, request, slug):
        size = request.GET.get('size')
        AboutCart.objects.filter(product=Product.objects.get(slug=slug), cart=request.user.cart, size=size).delete()
        return redirect('cart')


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'product/ordering.html'
    context_object_name = 'cart_items'

    def get(self, request, *args, **kwargs):
        if not AboutCart.objects.filter(cart=request.user.cart).exists():
            msg = _("You cannot order! First you need to add some products!")
            messages.warning(request, msg)
            return redirect('cart')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return AboutCart.objects.filter(cart=self.request.user.cart)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        subtotal = 0
        for item in self.get_queryset():
            subtotal += item.get_subtotal

        context['subtotal'] = subtotal
        return context

