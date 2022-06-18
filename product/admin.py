from django.contrib import admin
from .models import LoaiSanPham, ThuongHieu, SanPham, GiamGia, AnhSanPham, Comment, NhapKho, KhoangGia, SapXep
# Register your models here.


class SanPhamInline(admin.TabularInline):
    model = SanPham

@admin.register(LoaiSanPham)
class LoaiSanPhamAdmin(admin.ModelAdmin):
    list_display = ("MaLSP", "TenLSP")
    list_filter = ["TenLSP"]
    inlines = [SanPhamInline]

@admin.register(ThuongHieu)
class ThuongHieuAdmin(admin.ModelAdmin):
    list_display = ("MaTH", "TenTH", "XuatXu" ,"MoTa")
    list_filter = ("XuatXu", "TenTH")
    inlines = [SanPhamInline]

@admin.register(GiamGia)
class GiamGiaAdmin(admin.ModelAdmin):
    list_display = ("MaGG","MaSP","NgayBatDau","NgayKetThuc","PhanTram")
    list_filter = ("NgayBatDau","NgayKetThuc","PhanTram")

admin.site.register(AnhSanPham)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("MaCM","MaKH","MaSP","ChiTietCM","Rate","ThoiGian")
    list_filter = ("Rate", "ThoiGian")

@admin.register(NhapKho)
class NhapKhoInAdmin(admin.ModelAdmin):
    list_display = ("MaNhapKho","MaSP","SoLuong","NgayNhapKho","GiaNhap")
    list_filter = ("NgayNhapKho","GiaNhap")

@admin.register(SanPham)
class SanPhamAdmin(admin.ModelAdmin):
    list_display = ("MaSP","MaLSP","TenSP","NgSanXuat","HanSuDung","MaTH","Gia","SoLuong")
    list_filter = ("NgSanXuat","HanSuDung")

    # fieldsets = (
    #     (None, {
    #         "fields": ("MaSP", "TenSP","MaLSP")
    #     }),
    #     ("Availability", {
    #         "fields": ("Gia","SoLuong")
    #     }),
    # )
    

