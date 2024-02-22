from django.contrib import admin
from . models import  *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    
# Register your models here.
admin.site.register(CATEGORY, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','stock','available','created','updated']
    list_editable = ["price","stock","available"]
    prepopulated_fields = {"slug": ("name",)}
    list_per_page=20
admin.site.register(PRODUCTS,ProductAdmin)    
# Register your models here.
