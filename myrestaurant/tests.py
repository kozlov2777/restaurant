from django.test import TestCase
from myrestaurant.models import *


class CategoryModelTest(TestCase):

    def test_create_category(self):
        category = Category(id=1, name="test")
        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, "test")

    def test_category_str(self):
        category = Category(id=1, name="test")
        self.assertEqual(str(category), "test")


class MenuItemModelTest(TestCase):

    def test_menuitem_create(self):
        category = Category(id=1, name="test")
        menu_item = MenuItem(id=1, name="apple", description="green", price=10, category=category, image="")
        self.assertEqual(menu_item.id, 1)
        self.assertEqual(menu_item.name, "apple")
        self.assertEqual(menu_item.description, "green")
        self.assertEqual(menu_item.price, 10)
        self.assertEqual(menu_item.category, category)
        self.assertEqual(menu_item.image, "")

    def test_menuitems_str(self):
        category = Category(id=1, name="test")
        menu_item = MenuItem(id=1, name="apple", description="green", price=10, category=category, image="")
        self.assertEqual(str(menu_item), 'apple')


class IngredientModelTest(TestCase):
    def test_ingredient_create(self):
        ingredient = Ingredient(id=1, name="test", quantity= 10, unit="kg")
        self.assertEqual(ingredient.id, 1)
        self.assertEqual(ingredient.name, 'test')
        self.assertEqual(ingredient.quantity, 10)
        self.assertEqual(ingredient.unit, "kg")

