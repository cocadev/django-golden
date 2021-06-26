"""orderangel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from management import views
from django.conf.urls import url
from django.urls import path


urlpatterns = [

    # -------------------------------------------- Start Dashboard URLS ---------------------------------------------- #

    url(r'^$', views.secure_account, name="secure.home"),
    url(r'^employees/$', views.secure_employees, name="secure.employees"),
    url(r'^settings/$', views.secure_settings, name="secure.settings"),
    url(r'^clients/$', views.secure_clients, name="secure.clients"),
    url(r'^statistics/$', views.secure_statistics, name="secure.statistics"),
    url(r'^categories/$', views.secure_categories, name="secure.categories"),
    url(r'^orders/$', views.secure_orders, name="secure.orders"),
    url(r'^products/$', views.secure_products, name="secure.products"),
    url(r'^products/create/$', views.secure_product_creation, name="secure.product.create"),
    url(r'^products/create/pricing/$', views.secure_product_pricing, name="secure.product.pricing"),
    path('products/<int:id>/', views.secure_product_profile, name="secure.product.profile"),
    url(r'^employees/create/$', views.secure_employee_creation, name="secure.employee.create"),
    url(r'^employees/update/$', views.secure_employee_update, name="secure.employee.update"),
    path('employees/<int:id>/', views.secure_employee_profile, name="secure.employee.profile"),
    url(r'^api/employees/$', views.secure_employee_data_table, name="employees_dt"),
    url(r'^api/products/$', views.secure_products_data_table, name="products_dt"),
    url(r'^api/products/prices/$', views.prices, name="products_prices"),
    url(r'^api/products/statistics/$', views.secure_products_statistics, name="products_dt"),
    url(r'^product/update/$', views.secure_product_update, name="secure.product.update"),
    url(r'^categories/create/$', views.secure_category_creation, name="secure.category.create"),
    path('categories/<int:id>/', views.secure_category_profile, name="secure.category.profile"),
    path('categories/<int:cid>-products/', views.secure_category_products, name="secure.category.products"),
    path('orders/<int:id>/', views.secure_invoice_profile, name="secure.orders.profile"),
    path('orders/<str:id>/invoice', views.secure_invoice_download, name="secure.orders.download"),
    path('invoices/<int:id>/', views.secure_invoice_profile, name="secure.invoice.profile"),
    path('orders/update/', views.update_orders, name="secure.invoice.update"),
    path('orders/create/', views.create_order, name="secure.invoice.create"),
    url(r'^api/invoices/$', views.secure_invoices_data_table, name="invoice_product_dt"),
    url(r'^api/invoices/product/$', views.secure_invoices_data_table_product, name="invoice_dt"),
    url(r'^api/clients/$', views.secure_clients_data_table, name="clients_dt"),




    # -------------------------------------------- End Dashboard ---------------------------------------------------- #
]
