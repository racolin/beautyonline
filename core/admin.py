from django.contrib import admin
from .models import VanChuyen, Tinh, Huyen, Xa, KhachHang
# Register your models here.

admin.site.register(VanChuyen)
admin.site.register(Tinh)
admin.site.register(Xa)
admin.site.register(KhachHang)