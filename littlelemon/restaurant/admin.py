from django.contrib import admin
from .models import Menu, Category, MenuItem

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('name', 'price', 'description')
    
    # Sort the list view by the 'name' field in ascending order
    ordering = ('name',)