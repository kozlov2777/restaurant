from django.db import models
from django.utils import timezone


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)
    calories = models.FloatField()

    def __str__(self):
        return self.name


class IngredientItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"


class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)


class Table_Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Table(models.Model):
    id = models.AutoField(primary_key=True)
    table_status = models.ForeignKey(Table_Status, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Table {self.id}"


class Order(models.Model):
    table_id = models.ForeignKey(Table, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"







