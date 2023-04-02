from django.contrib import admin
from django.urls import path
from myrestaurant import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('all_order/', views.orders_view, name='view_order_list'),
    path('', views.order_by_status, name='order_by_status'),
    path('view_menu/', views.menu_view, name='view_menu_list'),
    path('category/', views.category_view, name='category_list'),
    path('new_order/', views.new_order, name='new_order'),
    path('salary/', views.employee_salary, name='salary'),
    path('tables/', views.tables_status, name='tables'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('item_detail/<int:order_id>/', views.item_detail, name='item_detail'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('update_order_status_and_table/<int:order_id>/', views.update_order_status_and_table, name='update_order_status_and_table'),
    path('order_detail_by_table_number/<int:table_number>/', views.order_detail_by_table_number, name='order_detail_by_table_number')
]
