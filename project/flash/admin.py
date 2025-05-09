from django.contrib import admin

from .models import *

class Categoryadmin(admin.ModelAdmin):
    list_display=('name','image','description','status')

class Productadmin(admin.ModelAdmin):
    list_display=('category','name','description','status','trending')


admin.site.register(Category,Categoryadmin)
admin.site.register(Product,Productadmin)
