from django.contrib import admin
from .models import LoaiSanPham, ThuongHieu, SanPham, GiamGia, AnhSanPham, Comment, NhapKho, KhoangGia, SapXep
# Register your models here.
admin.site.register(LoaiSanPham)
admin.site.register(ThuongHieu)
admin.site.register(GiamGia)
admin.site.register(AnhSanPham)
admin.site.register(Comment)
admin.site.register(NhapKho)
admin.site.register(KhoangGia)
admin.site.register(SapXep)
