from django.urls import reverse
from django.db import models

# Create your models here.
class CATEGORY(models.Model):
         name=models.CharField(max_length=250,unique=True)
         slug=models.SlugField(max_length=250,unique=True)
         description=models.TextField(blank=True)
         image=models.ImageField(upload_to='category', blank=True)


         class Meta:
             ordering = ('name',)
             verbose_name='category'
             verbose_name_plural='categories'

         def get_url(self):
            return reverse('shop:products_by_category',args=[self.slug])       

         def __str__(self):
                 return '{}'.format(self.name)

class PRODUCTS(models.Model):
       name=models.CharField(max_length=250,unique=True)
       slug=models.SlugField(max_length=250,unique=True)
       description=models.TextField(blank=True)
       price=models.DecimalField(max_digits=10, decimal_places=2)
       category=models.ForeignKey(CATEGORY, on_delete=models.CASCADE)
       image=models.ImageField(upload_to='product', blank=True)
       stock=models.IntegerField()
       available=models.BooleanField(default=True)
       created=models.DateTimeField(auto_now_add=True)
       updated=models.DateTimeField(auto_now=True)


       def get_url(self):
            return reverse('shop:prodcatdetail',args=[self.category.slug,self.slug]) 

       class Meta:
           ordering = ('name',)
           verbose_name=('Product')
           verbose_name_plural=('Products')




           def __str__(self):
               return '{}' .format(self.name) 


class Cart(models.Model):
      cart_id=models.CharField(max_length=255, blank=True)
      data_added=models.DateTimeField(auto_now_add=True)

      class Meta:
            db_table= "cart"
            ordering=["data_added"]

      def __str__(self):
            return '{}'.format(self.cart_id)
class Cartitem(models.Model):
      product=models.ForeignKey(PRODUCTS,on_delete=models.CASCADE) 
      cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
      quantity=models.PositiveIntegerField()
      active=models.BooleanField(default=True)

      class Meta:
            db_table='cartitem'
      def sub_total(self):
            return self.product.price * self.quantity
      def  __str__(self):
            return '{}'.format(self.product)  
           
       