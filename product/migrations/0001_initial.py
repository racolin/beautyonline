# Generated by Django 3.2 on 2021-05-09 01:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_auto_20210509_0814'),
    ]

    operations = [
        migrations.CreateModel(
            name='KhoHang',
            fields=[
                ('MaSP', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('SoLuong', models.IntegerField()),
            ],
            options={
                'db_table': 'KHOHANG',
            },
        ),
        migrations.CreateModel(
            name='LoaiSanPham',
            fields=[
                ('MaLSP', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('TenLSP', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'LOAISANPHAM',
            },
        ),
        migrations.CreateModel(
            name='ThuongHieu',
            fields=[
                ('MaTH', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('TenTH', models.CharField(max_length=20)),
                ('XuatXu', models.CharField(max_length=100)),
                ('MoTa', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'THUONGHIEU',
            },
        ),
        migrations.CreateModel(
            name='SanPham',
            fields=[
                ('MaSP', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('TenSP', models.CharField(max_length=100)),
                ('NgSanXuat', models.DateField()),
                ('HanSuDung', models.DateField()),
                ('MoTa', models.CharField(max_length=1000)),
                ('Gia', models.BigIntegerField()),
                ('MaLSP', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.loaisanpham')),
                ('MaTH', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.thuonghieu')),
            ],
            options={
                'db_table': 'SANPHAM',
            },
        ),
        migrations.CreateModel(
            name='NhapKho',
            fields=[
                ('MaNhapKho', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('SoLuong', models.IntegerField()),
                ('NgayNhapKho', models.DateField()),
                ('GiaNhap', models.BigIntegerField()),
                ('MaSP', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.sanpham')),
            ],
            options={
                'db_table': 'NHAPKHO',
            },
        ),
        migrations.CreateModel(
            name='GiamGia',
            fields=[
                ('MaGG', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('NgayBatDau', models.DateField()),
                ('NgayKetThuc', models.DateField()),
                ('PhanTram', models.FloatField()),
                ('MaSP', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.sanpham')),
            ],
            options={
                'db_table': 'GIAMGIA',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('MaCM', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('ChiTietCM', models.CharField(max_length=1000)),
                ('MaKH', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.khachhang')),
                ('MaSP', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.sanpham')),
            ],
            options={
                'db_table': 'COMMENT',
            },
        ),
        migrations.CreateModel(
            name='AnhSanPham',
            fields=[
                ('NguonAnh', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('LoaiAnh', models.BooleanField()),
                ('MaSP', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.sanpham')),
            ],
            options={
                'db_table': 'ANHSANPHAM',
            },
        ),
    ]
