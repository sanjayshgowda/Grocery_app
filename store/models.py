from django.db import models
from django.contrib.auth.models import User

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_cart_total(self):
        total = sum(item.get_total_price() for item in self.cartitem_set.all())
        return total
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.product.price * self.quantity
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
  