from django.db import models

from product.models import SanPham
from core.models import KhachHang, Xa 

# Create your models here.

class HoaDon(models.Model):
	MaHD = models.CharField(primary_key=True, max_length=20)
	MaKH = models.ForeignKey(KhachHang, on_delete=models.CASCADE, null=False)
	NgayDatHang = models.DateTimeField(null=False)
	ThanhTien = models.BigIntegerField(null=False)
	MaXaGH = models.ForeignKey(Xa, on_delete=models.CASCADE, null=False)
	TenNgNhan = models.CharField(max_length=50, null=True)
	SDTNgNhan = models.CharField(max_length=11, null=False)
	DiaChiNhan = models.CharField(max_length=100, null=False)
	VanChuyen = models.BigIntegerField(null=False)
	class Meta:
		db_table = 'HOADON'

class ChiTietHoaDon(models.Model):
	MaCTHD = models.CharField(primary_key=True, max_length=20)
	GiaBan = models.BigIntegerField(null=False)
	SoLuong = models.BigIntegerField(null=False)
	MaSP = models.ForeignKey(SanPham, on_delete=models.CASCADE, null=False)
	MaHD = models.ForeignKey(HoaDon, on_delete=models.CASCADE, null=False)
	class Meta:
		db_table = 'CHITIETHOADON'