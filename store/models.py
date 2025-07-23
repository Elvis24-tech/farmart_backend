from django.db import models
from core.models import TimestampedModel
from users.models import User

class AnimalCategory(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name
    class Meta:
        verbose_name_plural = "Animal Categories"

class Breed(TimestampedModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(AnimalCategory, on_delete=models.CASCADE, related_name='breeds')
    def __str__(self): return f"{self.name} ({self.category.name})"

class Animal(TimestampedModel):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='animals_for_sale', limit_choices_to={'user_type': User.UserType.FARMER})
    name = models.CharField(max_length=100)
    category = models.ForeignKey(AnimalCategory, on_delete=models.PROTECT)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT)
    age = models.IntegerField(help_text="Age in months")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image_url = models.URLField(max_length=500)
    is_sold = models.BooleanField(default=False)
    
    def __str__(self): return f"{self.name} - {self.breed.name}"

class Order(TimestampedModel):
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending Payment'
        PAID = 'PAID', 'Paid'
        FAILED = 'FAILED', 'Payment Failed'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    
    @property
    def total_price(self):
        return sum(item.price for item in self.items.all())

    def __str__(self): return f"Order {self.id} by {self.buyer.username}"

class OrderItem(TimestampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price at the time of order")
    
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.animal.price
        super().save(*args, **kwargs)

    def __str__(self): return f"{self.animal.name} in Order {self.order.id}"