from django.contrib import admin
from .models import AnimalCategory, Breed, Animal, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('animal', 'price') 
    extra = 0  
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'buyer__username', 'buyer__email')
    readonly_fields = ('buyer', 'created_at', 'total_price')
    inlines = [OrderItemInline]

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer', 'category', 'breed', 'price', 'is_sold')
    list_filter = ('is_sold', 'category', 'breed')
    search_fields = ('name', 'description', 'farmer__username')

@admin.register(AnimalCategory)
class AnimalCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)