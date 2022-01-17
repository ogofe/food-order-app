from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(StaffPermission)
admin.site.register(FoodItem)
admin.site.register(FoodImage)
admin.site.register(Customization)
admin.site.register(CustomizationOption)
admin.site.register(Associated)
admin.site.register(OrderCustomization)
admin.site.register(OrderItem)
admin.site.register(Notification)
