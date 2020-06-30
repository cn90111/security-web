"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('general/', include('general.urls')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('t_Closeness/', include('t_Closeness.urls')),
    path('DPSyn/', include('DPSyn.urls')),
    path('l_Diversity/', include('l_Diversity.urls')),
    path('k_Anonymity/', include('k_Anonymity.urls')),
    path('json_parser/', include('json_parser.urls')),
    path('accounts/', include('accounts.urls')),
)