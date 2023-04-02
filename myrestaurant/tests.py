from django.test import TestCase, Client
from myrestaurant.models import *
from django.urls import reverse


class MenuViewTestCase(TestCase):
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

    def test_menu_view_returns_200(self):
        response = self.client.get('/view_menu/')
        self.assertEqual(response.status_code, 200)

    def test_category_view_returns_200(self):
        response = self.client.get('/category/')
        self.assertEqual(response.status_code, 200)

    def test_orders_view_returns_200(self):
        response = self.client.get('/all_order/')
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

    def test_update_order_status(self):
        order_id = self.order.id
        response = self.client.get(reverse('update_order_status', kwargs={'order_id': order_id}))
        self.assertEqual(response.status_code, 302)
        updated_order = Order.objects.get(id=order_id)
        self.assertEqual(updated_order.status, self.status2)


