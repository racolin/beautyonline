from django.db import models
from django.db.models import UniqueConstraint

# Create your models here.

class VanChuyen(models.Model):
	MaKV = models.CharField(max_length=20, primary_key=True)
	Gia = models.BigIntegerField(null=False)
	class Meta:
		db_table = 'VANCHUYEN'

class Tinh(models.Model):
	MaTinh= models.CharField(max_length=20, primary_key=True)
	TenTinh= models.CharField(max_length=100, null=False)
	MaKV = models.ForeignKey(VanChuyen, on_delete=models.CASCADE, null=False)
	class Meta:
		db_table = 'TINH'

class Huyen(models.Model):
	MaHuyen = models.CharField(max_length=20, primary_key=True)
	TenHuyen = models.CharField(max_length=100, null=False)
	MaTinh = models.ForeignKey(Tinh, on_delete=models.CASCADE, null=False)
	class Meta:
		db_table = 'HUYEN'

class Xa(models.Model):
	MaXa = models.CharField(max_length=20, primary_key=True)
	TenXa = models.CharField(max_length=100, null=False)
	MaHuyen = models.ForeignKey(Huyen, on_delete=models.CASCADE, null=False)
	class Meta:
		db_table = 'XA'

class KhachHang(models.Model):
	MaKH = models.CharField(primary_key=True, max_length=20)
	Pass = models.CharField(max_length=20, null=False)
	TenKH = models.CharField(max_length=100, null=False)
	MaXa = models.ForeignKey(Xa, on_delete=models.CASCADE, null=True)
	DiaChi = models.CharField(max_length=100, null=False)
	SDT= models.CharField(max_length=11, null=True)
	Login = models.CharField(max_length=20, null=False)
	Email = models.CharField(max_length=50, null=False)
	class Meta:
		db_table = 'KHACHHANG'

class LienHe(models.Model):
	MaLH = models.AutoField(primary_key=True)
	HoTen = models.CharField(max_length=50, null=False)
	Email = models.CharField(max_length=50, null=False)
	SDT = models.CharField(max_length=11, null=False)
	NoiDung = models.CharField(max_length=500, null=False)
