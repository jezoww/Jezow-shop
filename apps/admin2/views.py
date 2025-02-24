from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, Q
from django.db.models.fields import IntegerField
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from apps.user.models import Order


class OperatorPageListView(LoginRequiredMixin, ListView):
    template_name = 'admin2/operator_panel.html'
    context_object_name = 'orders'

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return redirect('index')
        order_status = self.request.GET.get('order_status', 'all')
        if order_status == 'all':
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(status=order_status)

        search = self.request.GET.get('search')
        if search:
            orders = orders.filter(Q(id=search) | Q(user__phone=search))

        return orders

    def get_context_data(self, *, object_list=None, **kwargs):
        if not self.request.user.is_superuser:
            return redirect('index')
        context = super().get_context_data(object_list=object_list, **kwargs)
        order_status = self.request.GET.get('order_status')
        context['order_status'] = order_status
        return context


class ChangeStatusOrderView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not self.request.user.is_superuser:
            return redirect('index')
        order = Order.objects.get(id=pk)
        status = request.POST.get('status')
        order_status = request.GET.get('order_status')
        if status:
            order.status = status
            order.save()
            messages.success(request, "Saved!")

        base_url = reverse('operator')
        query_string = f"?order_status={order_status}"
        full_url = f"{base_url}{query_string}"
        return redirect(full_url)


class ChangeLocationOrderView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not self.request.user.is_superuser:
            return redirect('index')
        order = Order.objects.get(id=pk)
        location = request.POST.get('location')
        order_status = request.GET.get('order_status')
        if location:
            order.location = location
            order.save()
            messages.success(request, "Saqlandi!")

        base_url = reverse('operator')
        query_string = f"?order_status={order_status}"
        full_url = f"{base_url}{query_string}"
        return redirect(full_url)
