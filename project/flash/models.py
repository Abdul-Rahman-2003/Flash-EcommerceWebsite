from django.db import models
from django.contrib.auth.models import User
import datetime
import os


def getFileName(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    new_filename=f"{now_time}_{filename}"
    return os.path.join("uploads/",new_filename)


    
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    slug = models.SlugField(unique=True, blank=True, null=True)  # <-- ADD THIS
    image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            num = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    


from django.utils.text import slugify

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(unique=True,blank=True,null=True)  
    vendor = models.CharField(max_length=200, null=False, blank=False)
    product_image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False)
    orginal_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    trending = models.BooleanField(default=False, help_text="0-default,1-Trending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.vendor})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            num = 1
            # Ensure uniqueness
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
      return self.product_qty*self.product.selling_price
    
class Favourite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    



    