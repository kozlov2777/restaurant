from django.shortcuts import render

from django.db import connection
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import MenuItem, Order, OrderItem
from django.http import HttpResponseServerError


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
        cursor.execute('SELECT c.id, c.name, m.name, m.description, m.price FROM myrestaurant_category c JOIN myrestaurant_menuitem m ON m.category_id = c.id;')
        rows = cursor.fetchall()
        category_list = []
        for row in rows:
            category_list.append({
                'id': row[0],
                'name': row[1],
                'name1': row[2],
                'description': row[3],
                'price': row[4],
            })
    return render(request, "category_list.html", {'category_list': category_list})


def orders_view(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT o.id, o.table_id_id, o.created_at, SUM(oi.quantity * m.price) AS total_price FROM myrestaurant_order o JOIN myrestaurant_orderitem oi ON o.id = oi.order_id JOIN myrestaurant_menuitem m ON oi.item_id = m.id GROUP BY o.id ORDER BY o.created_at DESC')

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


def new_order(request):
    if request.method == 'POST':
        table_id_id = request.POST['table_id_id']
        employee_id = request.POST['employee_id']
        status_id = request.POST['status_id']
        items = request.POST.getlist('item')
        quantities = request.POST.getlist('quantity')

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO myrestaurant_order (table_id_id, created_at, employee_id, status_id) VALUES (%s, %s, %s, %s)", [table_id_id, timezone.now(), employee_id, status_id])
            order_id = cursor.lastrowid

            cursor.execute("UPDATE myrestaurant_table SET table_status_id = %s WHERE id = %s", [2, table_id_id])

            for i in range(len(items)):
                item_id = items[i]
                quantity = quantities[i]
                cursor.execute("INSERT INTO myrestaurant_orderitem (order_id, item_id, quantity) VALUES (%s, %s, %s)", [order_id, item_id, quantity])

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM myrestaurant_order WHERE id = %s", [order_id])
            order_data = cursor.fetchone()

            cursor.execute("SELECT myrestaurant_menuitem.*, myrestaurant_orderitem.quantity FROM myrestaurant_menuitem JOIN myrestaurant_orderitem ON myrestaurant_menuitem.id = myrestaurant_orderitem.item_id WHERE myrestaurant_orderitem.order_id = %s", [order_id])
            items_data = cursor.fetchall()

        order = Order(id=order_data[0], table_id_id=order_data[1], created_at=order_data[2], employee_id=order_data[3], status_id=order_data[4])
        order_items = [OrderItem(item=MenuItem(id=item[0], name=item[1], price=item[2]), quantity=item[3]) for item in items_data]

        return redirect('order_by_status')
    else:
        menu_items = MenuItem.objects.all()
        return render(request, 'new_order.html', {'menu_items': menu_items})


def order_detail(request, order_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT oi.id, oi.quantity, m.name, m.price FROM myrestaurant_orderitem oi JOIN myrestaurant_menuitem m ON oi.item_id = m.id WHERE oi.order_id =%s", [order_id]
            )
            rows = cursor.fetchall()
            if rows is None:
                return HttpResponseServerError('Order item does not exist.')
            else:
                detail_list = []
                for row in rows:
                    detail_list.append({
                        'id': row[0],
                        'quantity': row[1],
                        'item_name': row[2],
                        'item_price': row[3],
                    })
                return render(request, 'order_detail.html', {'detail_list': detail_list})
    except:
        return HttpResponseServerError('Error retrieving order item.')


def order_detail_by_table_number(request, table_number):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT o.id, m.name, oi.quantity, o.created_at, SUM(m.price * oi.quantity) as total FROM myrestaurant_order o INNER JOIN myrestaurant_orderitem oi ON o.id = oi.order_id INNER JOIN myrestaurant_menuitem m ON oi.item_id = m.id INNER JOIN myrestaurant_table t ON t.id=o.table_id_id WHERE t.id = %s GROUP BY o.id, m.id ORDER BY o.created_at DESC;",
            [table_number]
        )
        rows = cursor.fetchall()
        detail_by_table = []
        for row in rows:
            detail_by_table.append({
                'id': row[0],
                'name': row[1],
                'quantity': row[2],
                'created_at': row[3],
                'total': row[4],
            })
        return render(request, 'order_detail_by_table_number.html', {'detail_by_table': detail_by_table})


def order_by_status(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT o.id, o.table_id_id, m.name, oi.quantity, o.created_at, SUM(m.price * oi.quantity) as total, s.name, e.first_name FROM myrestaurant_order o INNER JOIN myrestaurant_orderitem oi ON o.id = oi.order_id INNER JOIN myrestaurant_menuitem m ON oi.item_id = m.id INNER JOIN myrestaurant_employee e ON o.employee_id = e.id INNER JOIN myrestaurant_status s ON o.status_id = s.id WHERE o.status_id = 1 GROUP BY o.id, m.id ORDER BY o.created_at DESC;"
        )
        rows = cursor.fetchall()
        order_by_status = []
        for row in rows:
            order_by_status.append({
                'id': row[0],
                'table_number': row[1],
                'name': row[2],
                'quantity': row[3],
                'created_at': row[4],
                'total': row[5],
                'status': row[6],
                'employee': row[7],
            })

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT o.id, o.table_id_id, m.name, oi.quantity, o.created_at, SUM(m.price * oi.quantity) as total, s.name, e.first_name FROM myrestaurant_order o INNER JOIN myrestaurant_orderitem oi ON o.id = oi.order_id INNER JOIN myrestaurant_menuitem m ON oi.item_id = m.id INNER JOIN myrestaurant_employee e ON o.employee_id = e.id INNER JOIN myrestaurant_status s ON o.status_id = s.id WHERE o.status_id = 2 GROUP BY o.id, m.id ORDER BY o.created_at DESC;"
        )
        rows = cursor.fetchall()
        order_by_status_2 = []
        for row in rows:
            order_by_status_2.append({
                'id': row[0],
                'table_number': row[1],
                'name': row[2],
                'quantity': row[3],
                'created_at': row[4],
                'total': row[5],
                'status': row[6],
                'employee': row[7],
            })

    return render(request, 'order_by_status.html', {'order_by_status': order_by_status, 'order_by_status_2': order_by_status_2})


def employee_salary(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT e.first_name, e.last_name, COUNT(o.id) * 30 AS salary FROM myrestaurant_order o JOIN myrestaurant_employee e ON o.employee_id = e.id GROUP BY e.id;");
        rows = cursor.fetchall()
        salary = []
        for row in rows:
            salary.append({
                'firstname': row[0],
                'secondname': row[1],
                'salary': row[2],
            })
        return render(request, 'salary.html' , {'salary': salary})


def tables_status(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT t.id, ts.name FROM myrestaurant_table t JOIN myrestaurant_table_status ts ON t.table_status_id=ts.id ORDER BY `t`.`id` ASC");
        rows = cursor.fetchall()
        tables = []
        for row in rows:
            tables.append({
                'id': row[0],
                'table_status_name': row[1],

            })
        return render(request, 'table_status.html' , {'tables': tables})


def update_order_status(request, order_id):
    with connection.cursor() as cursor:
        cursor.execute('UPDATE myrestaurant_order SET myrestaurant_order.status_id = 2 WHERE myrestaurant_order.id=%s ', [order_id])
    return redirect('order_by_status')


def update_order_status_and_table(request, order_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute('UPDATE myrestaurant_table SET table_status_id = 1 WHERE id = (SELECT table_id_id FROM myrestaurant_order WHERE id = %s);', [order_id])
    except Exception as e:
        print(f"Error in first query: {e}")
    try:
        with connection.cursor() as cursor:
            cursor.execute('UPDATE myrestaurant_order SET myrestaurant_order.status_id = 3 WHERE myrestaurant_order.id=%s ', [order_id])
    except Exception as e:
        print(f"Error in second query: {e}")
    return redirect('order_by_status')

