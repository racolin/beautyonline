from django.contrib import admin
from .models import ChiTietHoaDon, HoaDon
# Register your models here.
@admin.register(ChiTietHoaDon)
class ChiTietHoaDonAdmin(admin.ModelAdmin):
    list_display = ("MaCTHD","GiaBan","SoLuong","MaSP","MaHD")

class ChiTietHoaDonInline(admin.TabularInline):
    model = ChiTietHoaDon

@admin.register(HoaDon)
class HoaDonAdmin(admin.ModelAdmin):
    list_display = ("MaHD","MaKH","NgayDatHang","ThanhTien","MaXaGH","TenNgNhan","SDTNgNhan","DiaChiNhan","VanChuyen", "TrangThai")
    inlines = [ChiTietHoaDonInline]
