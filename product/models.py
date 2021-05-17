from django.db import models

from core.models import KhachHang

# Create your models here.

class LoaiSanPham(models.Model):
	MaLSP = models.CharField(primary_key=True, max_length=20)
	TenLSP = models.CharField(max_length=100, null=False)
	class Meta:
		db_table = 'LOAISANPHAM'

class ThuongHieu(models.Model):
	MaTH = models.CharField(primary_key=True, max_length=20)
	TenTH = models.CharField(max_length=20, null=False)
	XuatXu = models.CharField(max_length=100, null=False)
	MoTa = models.CharField(max_length=2000, null=False)
	class Meta:
		db_table = 'THUONGHIEU'

class SanPham(models.Model):
	MaSP = models.CharField(primary_key=True, max_length=20)
	MaLSP = models.ForeignKey(LoaiSanPham, on_delete=models.CASCADE, null=False)
	TenSP = models.CharField(max_length=100, null=False)
	NgSanXuat = models.DateField(null=False)
	HanSuDung = models.DateField(null=False)
	MaTH = models.ForeignKey(ThuongHieu, on_delete=models.CASCADE, null=False)
	MoTa = models.CharField(max_length=2000, null=False)
	Gia = models.BigIntegerField(null=False)
	SoLuong = models.IntegerField(null=False)
	class Meta:
		db_table = 'SANPHAM'

class GiamGia(models.Model):
	MaGG = models.CharField(primary_key=True, max_length=20)
	MaSP = models.ForeignKey(SanPham, on_delete=models.CASCADE, null=False)
	NgayBatDau = models.DateField(null=False)
	NgayKetThuc = models.DateField(null=False)
	PhanTram = models.FloatField(null=False)
	class Meta:
		db_table = 'GIAMGIA'

class AnhSanPham(models.Model):
	NguonAnh = models.CharField(primary_key=True, max_length=50)
	MaSP = models.ForeignKey(SanPham, on_delete=models.CASCADE, null=False)
	LoaiAnh = models.BooleanField()
	class Meta:
		db_table = 'ANHSANPHAM'

class Comment(models.Model):
	MaCM = models.AutoField(primary_key=True)
	MaKH = models.ForeignKey(KhachHang, on_delete=models.CASCADE, null=False)
	MaSP = models.ForeignKey(SanPham, on_delete=models.CASCADE, null=False)
	ChiTietCM = models.CharField(max_length=2000, null=False)
	Rate = models.IntegerField(null=False)
	ThoiGian = models.DateTimeField(null=False)
	class Meta:
		db_table = 'COMMENT'

class NhapKho(models.Model):
	MaNhapKho = models.CharField(primary_key=True, max_length=20)
	MaSP = models.ForeignKey(SanPham, on_delete=models.CASCADE, null=False)
	SoLuong = models.IntegerField(null=False)
	NgayNhapKho = models.DateField(null=False)
	GiaNhap = models.BigIntegerField(null=False)
	class Meta:
		db_table = 'NHAPKHO'

class KhoangGia(models.Model):
	MaKG = models.CharField(primary_key=True, max_length=10)
	Gia_Min = models.BigIntegerField(null=False)
	Gia_Max = models.BigIntegerField(null=False)
	class Meta:
		db_table = 'KHOANGGIA'

class SapXep(models.Model):
	MaSX = models.CharField(primary_key=True, max_length=50)
	TenSX = models.CharField(max_length=50)
	class Meta:
		db_table = 'SAPXEP'