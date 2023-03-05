from django.contrib import admin
from django.urls import path
from myrestaurant import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.orders_view, name='view_order_list'),
    path('view_menu/', views.menu_view, name='view_menu_list'),
    path('category/', views.category_view, name='category_list'),
    path('new_order/', views.new_order, name='new_order'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order_detail_by_table_number/<int:table_number>/', views.order_detail_by_table_number, name='order_detail_by_table_number')
]
