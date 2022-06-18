from django.contrib import admin
from .models import VanChuyen, Tinh, Huyen, Xa, KhachHang
# Register your models here.

@admin.register(VanChuyen)
class VanChuyenAdmin(admin.ModelAdmin):
    list_display = ("MaKV", "Gia")
    ordering = ["Gia"]

@admin.register(KhachHang)
class KhachHangAdmin(admin.ModelAdmin):
    list_display = ("MaKH","TenKH","DiaChi","SDT","Email","SignDate")
    search_fields = ["TenKH"]

