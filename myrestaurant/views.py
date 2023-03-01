from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.db import connection, transaction
from django.shortcuts import render


def menu_view(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT id, name, description, price FROM myrestaurant_menuitem')
        rows = cursor.fetchall()
        menu_list = []
        for row in rows:
            menu_list.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'price': row[3],
            })

    return render(request, 'menu.html', {'menu_list': menu_list})


def category_view(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT id, name, description, price, image FROM myrestaurant_menuitem WHERE category_id = 1')
        rows = cursor.fetchall()
        category_list = []
        for row in rows:
            category_list.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'price': row[3],
                'image': row[4]
            })
    return render(request, "category_list.html", {'category_list': category_list})


def orders_view(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT o.id, o.table_number, o.created_at, SUM(oi.quantity * m.price) AS total_price FROM myrestaurant_order o JOIN myrestaurant_orderitem oi ON o.id = oi.order_id JOIN myrestaurant_menuitem m ON oi.item_id = m.id GROUP BY o.id')

        rows = cursor.fetchall()
        order_list = []
        for row in rows:
            order_list.append({
                'id': row[0],
                'table_number': row[1],
                'created_at': row[2],
                'total': row[3],
            })
    return render(request, 'order_list.html', {'order_list': order_list})


def add_order_view(request):
    if request.method == 'POST':
        table_number = request.POST['table_number']
        created_at = request.POST['created_at']
        items = request.POST.getlist('item[]')
        quantities = request.POST.getlist('quantity[]')
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO myrestaurant_order (table_number, created_at) VALUES (%s, %s)', [table_number, created_at])
                order_id = cursor.lastrowid
                for i in range(len(items)):
                    cursor.execute('INSERT INTO myrestaurant_orderitem (order_id, item_id, quantity) VALUES (%s, %s, %s)', [order_id, items[i], quantities[i]])
        return HttpResponse('Order added successfully')
    else:
        with connection.cursor() as cursor:
            cursor.execute('SELECT id, name FROM menu')
            rows = cursor.fetchall()
            menu_items = []
            for row in rows:
                menu_items.append({
                    'id': row[0],
                    'name': row[1],
                })
        context = {'menu_items': menu_items}
        return HttpResponse(context)
