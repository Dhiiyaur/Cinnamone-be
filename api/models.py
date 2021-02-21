from django.db import models
from django.conf import settings

# Create your models here.

class Product(models.Model):

    product_name = models.CharField(max_length= 100)
    price = models.FloatField()
    # discount_price = models.FloatField(blank=True, null= True)
    # category = models.ForeignKey(CategoryItem, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='static/img/product', blank = True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField()

    def __str__(self):
        return self.product_name


class OrderProduct(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             blank=True, 
                             null= True)

    ordered = models.BooleanField(default=False)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.Product.product_name}"

    def get_total_price(self):
        return self.quantity * self.Product.price

    def get_final_price(self):
        
        return self.get_total_price()



class Order(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    Product = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total_price(self):

        total = 0
        for Product in self.Product.all():
            total += Product.get_final_price()

        return total