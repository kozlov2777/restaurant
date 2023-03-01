from django.contrib import admin
from django.urls import path
from myrestaurant import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_order/', views.add_order_view, name='add_order'),
    path('view_order_list/', views.orders_view, name='view_order_list'),
    path('view_menu/', views.menu_view, name='view_menu_list'),
    path('category/', views.category_view, name='category_list')
]
