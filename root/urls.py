"""
URL configuration for root project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.i18n import set_language

from root import settings

urlpatterns = [
    path('qwertyuiolmnbvcsdfhgdbsfwheacgfbehfbcuefgsjdbgfcejbfhncjhcnhfbcgfew/', admin.site.urls),
    path('ncndsufnucegfihfcrnc-0egu-ergcum-enrwnihce-jvmsbgfshdnc/', include('apps.admin2.urls')),
    path('set_language/', set_language, name='set_language'),
] + debug_toolbar_urls()

urlpatterns += i18n_patterns(
    path('', include('apps.user.urls')),
    path('product/', include('apps.product.urls')),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
