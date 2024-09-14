from django.db import models

def menu(request):
    from .models import Menu  # Import inside the function to avoid circular import
    menu_data = Menu.objects.all()
    return render(request, 'menu.html', {'menu': menu_data})

class Booking(models.Model):
    name = models.CharField(max_length=200)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()

    @property
    def reservation_slot(self):
        return f"{self.reservation_date} {self.reservation_time.strftime('%H:%M')}"

    def __str__(self):
        return f'{self.name}'

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)

    def __str__(self)-> str:
        return self.title
    

class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)

    def __str__(self)-> str:
        return self.title


class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, default='')
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # Ensures alphabetical order by the 'name' field
