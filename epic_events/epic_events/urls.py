"""epic_events URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import RedirectView
from epic_events.views import AccountListCreateView, AccountRUDView, ContractListCreateView, ContractRUDView, \
    EventRUDView, EventCreateView, AccountSearchView, ContractSearchView, EventSearchView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', RedirectView.as_view(url='accounts/'), name='home'),
     path('accounts/', AccountListCreateView.as_view(), name='account_list_create'),
    path('accounts/search/', AccountSearchView.as_view(), name='account_search'),
    path('contracts/search/', ContractSearchView.as_view(), name='contract_search'),
    path('events/search/', EventSearchView.as_view(), name='event_search'),
    path('accounts/<int:id>/', AccountRUDView.as_view(), name='account_RUD'),
    path('accounts/<int:id>/contracts/', ContractListCreateView.as_view(), name='contract_list_create'),
    path('accounts/<int:id>/contracts/<int:contract_id>/', ContractRUDView.as_view(), name='contract_RUD'),
    path('accounts/<int:id>/contracts/<int:contract_id>/event/', EventCreateView.as_view(), name='event_create'),
    path('accounts/<int:id>/contracts/<int:contract_id>/event/edit/', EventRUDView.as_view(), name='event_RUD'),
    

]