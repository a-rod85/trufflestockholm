from django.db import models

FOOD_MENU_SECTION = ((0, "Dinner"), (1, "New Item"))
DRINK_MENU_SECTION = ((0, "Beer"), (1, "Soft Drinks"))


class MenuSection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Food(models.Model):
    menu_section = models.ForeignKey(MenuSection, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Drink(models.Model):
    menu_section = models.ForeignKey(MenuSection, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
