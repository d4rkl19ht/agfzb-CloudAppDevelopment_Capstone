from django.contrib import admin
from .models import CarMake, CarModel



# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1

# CarModelAdmin class


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    # fields = []
    inlines = [CarModelInline]
    
# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel)