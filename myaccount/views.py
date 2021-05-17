from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from core.models import KhachHang, Xa, Huyen, Tinh
from myaccount.models import ChiTietHoaDon, HoaDon
from product.models import Comment, SanPham
from django.db.models import Q
from django.core.mail import send_mail
from product.views import getCommemt, get_Item_By_O
from core.support import convertCurrency
from django.db import transaction
from core.support import displayCart
from datetime import datetime
# Create your views here.

class MyAccount(View):
    def get(self, request):
        username = get_username(request)
        if username == "":
            return redirect('login')
        phone = KhachHang.objects.filter(MaKH__exact=username).first().SDT
        phone = phone or ""
        content = {'name_user': get_name(request), 'username': username, 'phone': phone}
        carts, total = displayCart(request.session.get('carts', ""))
        content['carts'] = carts
        content['total'] = convertCurrency(total)
        content['amount'] = len(request.session.get('carts', []))
        return render(request, 'site/pages/thong-tin-tai-khoan.html', content)

class MyOrders(View):
    def get(self, request):
        username = get_username(request)
        if username == "":
            return redirect('login')
        phone = KhachHang.objects.filter(MaKH__exact=username).first().SDT
        phone = phone or ""
        content = {'name_user': get_name(request), 'username': username, 'phone': phone}
        orders = HoaDon.objects.filter(MaKH__MaKH__exact=username).values('MaHD', 'NgayDatHang')
        list_orders_detail = []
        i = len(orders)
        for order in reversed(orders):
            list_orders_detail.append({'MaHD': order['MaHD'], 'index': i, 'NgayDatHang': order['NgayDatHang'], 'order_details': get_Detail_Order(order['MaHD'])})
            i -= 1
        content['orders'] = list_orders_detail
        carts, total = displayCart(request.session.get('carts', ""))
        content['carts'] = carts
        content['total'] = convertCurrency(total)
        content['amount'] = len(request.session.get('carts', []))
        return render(request, 'site/pages/don-hang-cua-toi.html', content)

class MyAddress(View):
    def get(self, request):
        username = get_username(request)
        if username == "":
            return redirect('login')
        phone = KhachHang.objects.filter(MaKH__exact=username).first().SDT
        phone = phone or ""
        content = {'name_user': get_name(request), 'username': username, 'phone': phone}
        khachhang = KhachHang.objects.filter(MaKH__exact=username).first()
        xa = khachhang.MaXa
        tinhs = Tinh.objects.all().values('MaTinh', 'TenTinh')
        content['Tinhs'] = tinhs
        if xa:
            huyen = xa.MaHuyen
            tinh = huyen.MaTinh
            diachi = khachhang.DiaChi
            content['Xa'] = xa
            content['Huyen'] = huyen
            content['Tinh'] = tinh
            content['DiaChi'] = diachi
        carts, total = displayCart(request.session.get('carts', ""))
        content['carts'] = carts
        content['total'] = convertCurrency(total)
        content['amount'] = len(request.session.get('carts', []))
        return render(request, 'site/pages/dia-chi-giao-hang-mac-dinh.html', content)

@csrf_exempt
def getMoreComment(request):
    current_comment = request.POST.get('current_comment', '0')
    id_product = request.POST.get('id_product', '')
    content = {}
    content['current_comment'], content['still'], content['comments'] = getCommemt(id_product, int(current_comment))
    return JsonResponse(content)

def addComment(request):
    mode = request.POST.get("mode", "")
    MaSP = request.POST.get("MaSP", "")
    rate = request.POST.get("rating", "")
    description = request.POST.get("description", "")
    thoigian = datetime.now()
    username = get_username(request)
    if username == "":
        return redirect('login')
    kh = KhachHang.objects.filter(MaKH__exact=username).first()
    sp = SanPham.objects.filter(MaSP__exact=MaSP).first()
    cm = Comment()
    cm.Rate = rate
    cm.MaSP = sp
    cm.MaKH = kh
    cm.ThoiGian = thoigian
    cm.ChiTietCM = description
    cm.save()
    return redirect('mode.item', mode=mode, id_product=MaSP)

@transaction.atomic
def getOrder(request):

    MaXa = request.POST.get("ward", "")
    DiaChi = request.POST.get("address", "")
    SDTNgNhan = request.POST.get('mobile', "")
    TenNgNhan = request.POST.get('fullname', '')
    
    username = get_username(request)
    index = HoaDon.objects.all().count() + 1
    id_order = "HD" + str(index).zfill(5)

    carts, total = displayCart(request.session.get('carts', ""))
    total = 0
    for cart in carts:
        cart['price_sale'] = int("".join(cart['price_sale'].split(",")))
        amount_product = cart['amount']
        total += amount_product * cart['price_sale']
    
    order = HoaDon()
    order.MaHD = id_order
    order.NgayDatHang = datetime.now()
    order.ThanhTien = total
    order.MaKH = KhachHang.objects.filter(MaKH__exact=get_username(request)).first()
    order.MaXaGH = Xa.objects.filter(MaXa__exact=MaXa).first()
    order.DiaChiNhan = DiaChi
    order.SDTNgNhan = SDTNgNhan
    order.TenNgNhan = TenNgNhan
    order.VanChuyen = Xa.objects.filter(MaXa__exact=MaXa).first().MaHuyen.MaTinh.MaKV.Gia

    order.save()

    index = ChiTietHoaDon.objects.all().count()
    for cart in carts:
        index += 1
        order_detail = ChiTietHoaDon()
        order_detail.MaCTHD = "CTHD" + str(index).zfill(6)
        order_detail.GiaBan = cart['price_sale']
        order_detail.SoLuong = cart['amount']
        order_detail.MaHD = order
        order_detail.MaSP = SanPham.objects.filter(MaSP__exact=cart['product']['MaSP']).first()
        order_detail.save()

    index = HoaDon.objects.filter(MaKH__MaKH__exact=username).count()
    del request.session['carts']
    return redirect('myaccount.detailorder', id_order=id_order, index=index)
    

def Signup(request):
    name = request.POST['name']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    login = 'form'
    khachhang = KhachHang()
    khachhang.Email = email
    khachhang.TenKH = name
    khachhang.MaKH = username
    khachhang.Pass = password
    khachhang.Login = login
    kh = KhachHang.objects.filter(Q(MaKH__exact=username) | Q(Email__exact=email)).first()
    if kh:
        return render(request, 'site/pages/signup.html')
    else:
        khachhang.save()
        request.session['name'] = name
        request.session['username'] = username
        return redirect('myaccount.address')
    
def EditInfo(request):
    old_password = request.POST.get('old_password', "")
    password = request.POST.get('password', "")
    name = request.POST.get('fullname', "")
    phone = request.POST.get('mobile', "")
    username = request.session.get('username', "")
    khachhang = KhachHang.objects.filter(MaKH__exact=username, Pass__exact=old_password)
    if khachhang.count() != 0:
        khachhang = khachhang.first()
        if password != "":
            khachhang.Pass = password
        if name != "":
            khachhang.TenKH = name
        if phone != "":
            khachhang.SDT = phone
        khachhang.save()
        request.session['name'] = name
    return redirect('myaccount.info')

def EditAddress(request):
    ward = request.POST.get('ward', "")
    housenumber_street = request.POST.get('housenumber_street', "")

    username = request.session.get('username', "")
    khachhang = KhachHang.objects.filter(MaKH__exact=username)
    if khachhang.count() != 0:
        khachhang = khachhang.first()
        if ward != "":
            khachhang.MaXa = Xa.objects.filter(MaXa__exact=ward).first()
        if housenumber_street != "":
            khachhang.DiaChi = housenumber_street
        khachhang.save()
    return redirect('myaccount.address')

def Login(request):
    username = request.POST['username']
    password = request.POST['password']
    khachhang = KhachHang.objects.filter(MaKH__exact=username, Pass__exact=password).first()
    if khachhang:
        request.session['name'] = khachhang.TenKH
        request.session['username'] = username
        return redirect('home')
    return render(request, 'site/pages/login.html', {'message':'Tài khoản hoặc mật khẩu không đúng!'})
    
def DetailOrder(request, *args, **kwargs):
    username = get_username(request)
    if username == "":
        return redirect('login')
    phone = KhachHang.objects.filter(MaKH__exact=username).first().SDT
    phone = phone or ""
    content = {'name_user': get_name(request), 'username': username, 'phone': phone}
    id_order = kwargs.get("id_order", "")
    index = kwargs.get("index", "")
    order = {}
    if index != "" and id_order != "":
        hoadon = HoaDon.objects.filter(MaHD__exact=id_order).first()
        xa = hoadon.MaXaGH
        Xa = xa.TenXa
        Huyen = xa.MaHuyen.TenHuyen
        Tinh = xa.MaHuyen.MaTinh.TenTinh
        if hoadon:
            order = {'orderinfo': convertHoaDonToObject(hoadon), 'index': index, 'xa': Xa, 'huyen': Huyen, 'tinh': Tinh, 'order_details': get_Detail_Order(id_order)}
    content['order'] = order
    carts, total = displayCart(request.session.get('carts', ""))
    content['carts'] = carts
    content['index'] = index
    content['total'] = convertCurrency(total)
    content['amount'] = len(request.session.get('carts', []))
    return render(request, 'site/pages/chi-tiet-don-hang.html', content)
    
def convertHoaDonToObject(hoadon: HoaDon):
    hd = {}
    hd['NgayDatHang'] = hoadon.NgayDatHang
    hd['ThanhTien'] = hoadon.ThanhTien
    hd['VanChuyen'] = hoadon.VanChuyen
    hd['TenNgNhan'] = hoadon.TenNgNhan
    hd['SDTNgNhan'] = hoadon.SDTNgNhan
    hd['DiaChiNhan'] = hoadon.DiaChiNhan
    hd['TongTien'] = convertCurrency(hd['ThanhTien'] + hd['VanChuyen'])
    hd['ThanhTien'] = convertCurrency(hd['ThanhTien'])
    hd['VanChuyen'] = convertCurrency(hd['VanChuyen'])
    return hd

def get_Detail_Order(MaHD):
    cthds = ChiTietHoaDon.objects.filter(MaHD__MaHD__exact=MaHD)
    order_details = []
    for cthd in cthds:
        product = get_Item_By_O(cthd.MaSP)
        order_details.append({'amount': cthd.SoLuong, 'product': product, 'total': convertCurrency(cthd.SoLuong * cthd.GiaBan)})
    return order_details

def Forget(request):
    email = request.POST['email']
    khachhang = KhachHang.objects.filter(Email__exact=email).first()
    if khachhang:
        password = khachhang.Pass
        send_mail(
            'Beaute Online send your password',
            'Password: ' + password,
            'beautyonline191101@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect('login')
    return redirect('home')

def Logout(request):
    del request.session['name']
    return redirect('home')

def get_name(request):
    return request.session.get('name', "")

def get_username(request):
    return request.session.get('username', "")