from django.test import TestCase, Client
from myrestaurant.models import *
from django.urls import reverse


class ModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(
            name='test')
        menu_item = MenuItem.objects.create(
            name='test',
            description='test',
            price=5.99,
            category=category,
            image=None
        )
        ingredient = Ingredient.objects.create(
            name='test',
            quantity=100,
            unit='grm',
            calories=0.52
        )
        ingredient_item = IngredientItem.objects.create(
            item=menu_item,
            ingredient=ingredient,
            quantity=3,
            unit='test'
        )
        status = Status.objects.create(
            name='test'
        )
        role = Role.objects.create(
            name='test'
        )
        employee = Employee.objects.create(
            first_name='test',
            last_name='test',
            role=role

        )
        table_status = Table_Status.objects.create(
            name='test'
        )
        table = Table.objects.create(
            table_status=table_status
        )
        order = Order.objects.create(
            table_id=table,
            created_at=timezone.now(),
            status=status,
            employee=employee
        )
        order.items.add(menu_item)
        order_item = OrderItem.objects.create(
            order=order,
            item=menu_item,
            quantity=1
        )

    def test_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)

    def test_mi_name_max_length(self):
        menu_items = MenuItem.objects.get(id=1)
        max_length = menu_items._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)

    def test_i_name_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)

    def test_employee_first_name_max_length(self):
        employee = Employee.objects.get(id=1)
        max_length = employee._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 50)

    def test_employee_last_name_max_length(self):
        employee = Employee.objects.get(id=1)
        max_length = employee._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 50)

    def test_i_unit_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field('unit').max_length
        self.assertEqual(max_length, 50)

    def test_status_name_max_length(self):
        status = Status.objects.get(id=1)
        max_length = status._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_role_name_max_length(self):
        role = Role.objects.get(id=1)
        max_length = role._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_table_status_name_max_length(self):
        table_status = Table_Status.objects.get(id=1)
        max_length = table_status._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_ii_unit_max_length(self):
        ingredient_item = IngredientItem.objects.get(id=1)
        max_length = ingredient_item._meta.get_field('unit').max_length
        self.assertEqual(max_length, 50)

    def test_category_name(self):
        category = Category.objects.get(id=1)
        expected_name = f'{category.name}'
        self.assertEqual(expected_name, str(category))

    def test_mi_name(self):
        menu_items = MenuItem.objects.get(id=1)
        expected_name = f'{menu_items.name}'
        self.assertEqual(expected_name, str(menu_items))

    def test_mi_price(self):
        menu_item = MenuItem.objects.get(id=1)
        expected_price = '5.99'
        self.assertEqual(expected_price, str(menu_item.price))

    def test_i_quantity(self):
        ingredient = Ingredient.objects.get(id=1)
        expected_quantity = '100.0'
        self.assertEqual(expected_quantity, str(ingredient.quantity))

    def test_oi_quantity(self):
        order_item = OrderItem.objects.get(id=1)
        expected_quantity = '1'
        self.assertEqual(expected_quantity, str(order_item.quantity))

    def test_i_calories(self):
        ingredient = Ingredient.objects.get(id=1)
        expected_calories = '0.52'
        self.assertEqual(expected_calories, str(ingredient.calories))

    def test_ii_quantity(self):
        ingredient_item = IngredientItem.objects.get(id=1)
        expected_quantity = '3'
        self.assertEqual(expected_quantity, str(ingredient_item.quantity))



    def test_menu_item_category(self):
        menu_item = MenuItem.objects.get(id=1)
        category = menu_item.category
        expected_category_name = 'test'
        self.assertEqual(expected_category_name, category.name)

    def test_order_table(self):
        order = Order.objects.get(id=1)
        table = order.table_id
        expected_table = 1
        self.assertEqual(expected_table, table.id)

    def test_order_employee(self):
        order = Order.objects.get(id=1)
        employee = order.employee.id
        expected_employee = 1
        self.assertEqual(expected_employee, employee)

    # def test_order_item(self):
    #     order = Order.objects.get(id=1)
    #     item = order.items.name
    #     expected_item = 'test'
    #     self.assertEqual(expected_item, item)

    def test_order_created(self):
        order = Order.objects.get(id=1)
        created_at = order.created_at.year
        created_at1 = order.created_at.month
        created_at2 = order.created_at.day
        created_at3 = order.created_at.hour
        created_at4 = order.created_at.minute
        expected_time = timezone.now().year
        expected_time1 = timezone.now().month
        expected_time2 = timezone.now().day
        expected_time3 = timezone.now().hour
        expected_time4 = timezone.now().minute
        self.assertEqual(expected_time, created_at)
        self.assertEqual(expected_time1, created_at1)
        self.assertEqual(expected_time2, created_at2)
        self.assertEqual(expected_time3, created_at3)
        self.assertEqual(expected_time4, created_at4)


    def test_ii_items(self):
        ingredient_item = IngredientItem.objects.get(id=1)
        item = ingredient_item.item
        expected_item_name = 'test'
        self.assertEqual(expected_item_name, item.name)

    def test_ii_ingredient(self):
        ingredient_item = IngredientItem.objects.get(id=1)
        ingredient = ingredient_item.ingredient
        expected_ingredient_name = 'test'
        self.assertEqual(expected_ingredient_name, ingredient.name)

    def test_employee_role(self):
        employee = Employee.objects.get(id=1)
        role = employee.role
        expected_role = 'test'
        self.assertEqual(expected_role, role.name)

    def test_table_table_status(self):
        table = Table.objects.get(id=1)
        table_status = table.table_status
        expected_status = 'test'
        self.assertEqual(expected_status, table_status.name)

    def test_order_item_order(self):
        order_item = OrderItem.objects.get(id=1)
        order = order_item.order.id
        expected_id = 1
        self.assertEqual(expected_id, order)

    def test_order_item_item(self):
        order_item = OrderItem.objects.get(id=1)
        item = order_item.item.id
        expected_id = 1
        self.assertEqual(expected_id, item)




    def test_menu_item_description(self):
        menu_item = MenuItem.objects.get(id=1)
        expected_description = 'test'
        self.assertEqual(expected_description, menu_item.description)

    # def test_menu_item_image_upload(self):
    #     menu_item = MenuItem.objects.get(id=1)
    #     self.assertIsNone(menu_item.image)


class ViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.category = Category.objects.create(name='test_category')
        cls.ingredient = Ingredient.objects.create(name='test_ingredient', quantity=100, unit='grm', calories=56)
        cls.menu_item = MenuItem.objects.create(name='test_item', description='test_description', price=10, category=cls.category)
        cls.ingredient_item = IngredientItem.objects.create(item=cls.menu_item, ingredient=cls.ingredient,  quantity=2)
        cls.status1 = Status.objects.create(name='test_status1')
        cls.status2 = Status.objects.create(name='test_status2')
        cls.role = Role.objects.create(name='test_role')
        cls.employee = Employee.objects.create(first_name="test_first_name", last_name='test_last_name', role=cls.role)
        cls.table_status1 = Table_Status.objects.create(name='test_table_status1')
        cls.table_status2 = Table_Status.objects.create(name='test_table_status2')
        cls.table = Table.objects.create(table_status=cls.table_status1)
        cls.order = Order.objects.create(table_id=cls.table, created_at=timezone.now(), status=cls.status1, employee=cls.employee)
        cls.order_item = OrderItem.objects.create(order=cls.order, item=cls.menu_item, quantity=2)
        cls.order_count = 1
    def test_menu_view_returns_200(self):
        response = self.client.get('/view_menu/')
        self.assertEqual(response.status_code, 200)

    def test_category_view_returns_200(self):
        response = self.client.get('/category/')
        self.assertEqual(response.status_code, 200)

    def test_orders_view_returns_200(self):
        response = self.client.get('/all_order/')
        self.assertEqual(response.status_code, 200)

    def test_order_detail_view_returns_200(self):
        response = self.client.get(f'/order/{self.order.id}/')
        self.assertEqual(response.status_code, 200)

    def test_order_detail_by_table_number_view_returns_200(self):
        response = self.client.get(f'/order_detail_by_table_number/{self.table.id}/')
        self.assertEqual(response.status_code, 200)

    def test_order_by_status_returns_200(self):
        response = self.client.get('//')
        self.assertEqual(response.status_code, 200)

    def test_employee_salary_returns_200(self):
        response = self.client.get('/salary/')
        self.assertEqual(response.status_code, 200)

    def test_table_status_returns_200(self):
        response = self.client.get('/tables/')
        self.assertEqual(response.status_code, 200)

    def test_item_detail_returns_200(self):
        response = self.client.get(f'/item_detail/{self.table.id}/')
        self.assertEqual(response.status_code, 200)

    def test_category_view_returns_category_view(self):
        response = self.client.get('/category/')
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.menu_item.name)
        self.assertContains(response, self.menu_item.description)
        self.assertContains(response, self.menu_item.price)

    def test_menu_view_returns_menu_item(self):
        response = self.client.get('/view_menu/')
        self.assertContains(response, self.menu_item.name)
        self.assertContains(response, self.menu_item.description)
        self.assertContains(response, self.menu_item.price)
        self.assertContains(response, self.menu_item.category.name)
        self.assertContains(response, self.ingredient.calories * self.ingredient_item.quantity)

    def test_orders_view_returns_orders_view(self):
        response = self.client.get('/all_order/')
        self.assertContains(response, self.order.table_id.id)
        self.assertContains(response, self.order.created_at.year)
        self.assertContains(response, self.order.created_at.month.imag)
        self.assertContains(response, self.order.created_at.day)
        self.assertContains(response, self.order.created_at.hour)
        self.assertContains(response, self.order.created_at.minute)
        self.assertContains(response, self.order_item.quantity*self.menu_item.price)

    def test_order_detail(self):
        response = self.client.get(f'/order/{self.order.id}/')
        self.assertTemplateUsed(response, 'order_detail.html')
        self.assertContains(response, self.menu_item.name)
        self.assertContains(response, self.order_item.quantity)
        self.assertContains(response, self.menu_item.price)

    def test_order_detail_by_table_number(self):
        response = self.client.get(f'/order_detail_by_table_number/{self.table.id}/')
        self.assertTemplateUsed(response, 'order_detail_by_table_number.html')
        self.assertContains(response, self.menu_item.name)
        self.assertContains(response, self.order_item.quantity)
        self.assertContains(response, self.order.created_at.year)
        self.assertContains(response, self.order.created_at.month.imag)
        self.assertContains(response, self.order.created_at.day)
        self.assertContains(response, self.order.created_at.hour)
        self.assertContains(response, self.order.created_at.minute)
        self.assertContains(response, self.menu_item.price*self.order_item.quantity)

    def test_order_by_status_returns_orders_view(self):
        response = self.client.get('//')
        self.assertContains(response, self.order.table_id.id)
        self.assertContains(response, self.menu_item.name)
        self.assertContains(response, self.order_item.quantity)
        self.assertContains(response, self.order.created_at.year)
        self.assertContains(response, self.order.created_at.month.imag)
        self.assertContains(response, self.order.created_at.day)
        self.assertContains(response, self.order.created_at.hour)
        self.assertContains(response, self.order.created_at.minute)
        self.assertContains(response, self.order_item.quantity*self.menu_item.price)

    def test_employee_salary_returns_employee_salary(self):
        response = self.client.get('/salary/')
        self.assertContains(response, self.employee.first_name)
        self.assertContains(response, self.employee.last_name)
        expected_salary = self.order_count * 30 + 12000
        self.assertContains(response, expected_salary)

    def test_employee_salary_returns_employee_salary(self):
        response = self.client.get('/tables/')
        self.assertContains(response, self.table.id)
        self.assertContains(response, self.table.table_status)

    def test_item_detail_returns_200(self):
        response = self.client.get(f'/item_detail/{self.order.id}/')
        self.assertContains(response, self.menu_item.name)
        self.assertContains(response, self.ingredient_item.quantity)
        self.assertContains(response, self.ingredient.name)
        self.assertContains(response, self.ingredient_item.unit)
        self.assertContains(response, self.ingredient.calories)


    def test_update_order_status(self):
        order_id = self.order.id
        response = self.client.get(reverse('update_order_status', kwargs={'order_id': order_id}))
        self.assertEqual(response.status_code, 302)
        updated_order = Order.objects.get(id=order_id)
        self.assertEqual(updated_order.status, self.status2)

    def test_update_order_status_and_table(self):
        url = reverse('update_order_status_and_table', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Table.objects.get(id=self.table_status1.id).table_status.name, 'test_table_status1')
        self.assertEqual(Status.objects.get(id=self.status1.id).name, 'test_status1')




