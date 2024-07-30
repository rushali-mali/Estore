from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    CAT=((1,'Mobile'),(2,'Cloth'),(3,'Shoes'))
    name=models.CharField(max_length=50)
    price=models.FloatField()
    pdetails=models.CharField(max_length=100, verbose_name="product details")
    cat=models.IntegerField(verbose_name="category", choices=CAT)
    is_active=models.BooleanField(default=True,verbose_name="Available")
    pimage = models.ImageField(upload_to='image')
    def _str_(self):
        return self.name
    
class Cart(models.Model):
    uid = models.ForeignKey(User, on_delete = models.CASCADE, db_column = 'uid')
    pid = models.ForeignKey(Product, on_delete = models.CASCADE, db_column = 'pid')    
    qty = models.IntegerField(default=1)

class Order(models.Model):
    order_id = models.CharField(max_length=50)
    uid = models.ForeignKey(User, on_delete = models.CASCADE, db_column = 'uid')
    pid = models.ForeignKey(Product, on_delete = models.CASCADE, db_column = 'pid')    
    qty = models.IntegerField(default=1)