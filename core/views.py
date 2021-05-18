from django.shortcuts import redirect, render
from django.views import View
from product.models import LoaiSanPham, SanPham, AnhSanPham, NhapKho, GiamGia
from .models import KhachHang, LienHe, Tinh, Huyen, Xa
from myaccount.models import ChiTietHoaDon, HoaDon
from core.support import convertCurrency
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from product.views import get_Item, get_Item_By_O
from django.db.models import Count
from datetime import datetime, timedelta

# Create your views here.

# hàm bổ trợ
# thêm sản theo tất cả các loại 
def addCategory():
    types = []
    images = AnhSanPham.objects.filter(LoaiAnh__exact=1).values_list('MaSP', 'NguonAnh')
    product_types = LoaiSanPham.objects.all()
    temp = 'dsdsa'
    for product_type in product_types:
        products = SanPham.objects.filter(MaLSP__TenLSP__exact=product_type.TenLSP)
        products_images = []
        for product in products:
            product_image = {}
            product_image = product
            price_sale = GiamGia.objects.filter(MaSP__exact=product.MaSP, NgayKetThuc__gt=datetime.now()).first()
            price_rate = price_sale.PhanTram if price_sale else 0
            price_sale = convertCurrency(int((1 - price_rate) * product.Gia ))
            product_image.Gia = convertCurrency(product_image.Gia)
            for image in images:
                if product.MaSP == image[0]:
                    products_images.append({'product': product_image, 'image': image[1], 'price_sale': price_sale})
                    break
        types.append({'name': product_type.TenLSP, 'products_images': products_images})
    return types

# lấy thông tin searh của khách để tìm sản phẩm phù hợp
@csrf_exempt
def getSearch(request):
    search = request.POST.get('search', "")
    sps = SanPham.objects.filter(TenSP__icontains=search)[:10]
    result = []
    for sp in sps:
        result.append({'MaSP': sp.MaSP, 'TenSP': sp.TenSP})
        
    return JsonResponse({'result': result})
# chuyển hướng đến trang đặt hàng
# nếu đã đăng nhập thì chuyển đến trang đặt hàng, nếu không thì chuyển đến trang login   
class Order(View):
    def get(self, request):
        username = get_username(request)
        if username == "":
            return redirect('login')
        name = get_name(request)
        carts, total = displayCart(request.session.get('carts', ""))
        khachhang = KhachHang.objects.filter(MaKH__exact=username).first()
        xa = khachhang.MaXa
        transport = 0
        content = {}
        if xa:
            content['Xa'] = xa
            content['Huyen'] = xa.MaHuyen
            content['Tinh'] = xa.MaHuyen.MaTinh.MaTinh
            content['DiaChi'] = khachhang.DiaChi
            transport = xa.MaHuyen.MaTinh.MaKV.Gia

        content['Tinhs'] = Tinh.objects.all().values('MaTinh', 'TenTinh')
        content['transport'] = convertCurrency(transport)
        content['totalAll'] = convertCurrency(transport + total)
        content['name_user'] = name
        content['phone'] = khachhang.SDT
        content['carts'] = carts
        content['total'] = convertCurrency(total)
        content['amount'] = len(request.session.get('carts', []))
        return render(request, 'site/pages/dat-hang.html', content) 

# chuyển hướng đến trang home
class Home(View):
    def get(self, request):
        # Thêm các loại sản phẩm
        types = addCategory()
        # Thêm sản phẩm bán chạy
        temp = HoaDon.objects.filter(NgayDatHang__gte=datetime.now() - timedelta(days=60)).values('MaHD')
        hoadon = []
        for tem in temp:
            hoadon.append(tem['MaHD'])
        cthds = []
        cthds = ChiTietHoaDon.objects.filter(MaHD__in=hoadon).values('MaSP').annotate(TongSL=Count('SoLuong')).order_by('-TongSL')
        
        id_selling_products = []
        for cthd in cthds:
            id_selling_products.append(cthd['MaSP'])
        selling_products = SanPham.objects.filter(MaSP__in=id_selling_products)
        products_images = []
        for selling_product in selling_products:
            products_images.append(get_Item_By_O(selling_product))
        types.insert(0, {'name': 'Sảm phẩm bán chạy', 'products_images': products_images})

        # Thêm sản phẩm giảm giá
        sales = []
        sales = GiamGia.objects.filter(NgayKetThuc__gte=datetime.now())

        id_sale_products = []
        for sale in sales:
            id_sale_products.append(sale.MaSP.MaSP)
        
        sale_products = SanPham.objects.filter(MaSP__in=id_sale_products)
        products_images = []
        for sale_product in sale_products:
            products_images.append(get_Item_By_O(sale_product))
        types.insert(0, {'name': 'Sảm phẩm giảm giá', 'products_images': products_images})
        # Tạo thêm sản phẩm mới nhất
        store = NhapKho.objects.order_by('-NgayNhapKho')[:8].values_list('MaSP')
        new_products = SanPham.objects.filter
        new_keys = []
        for k in store:
            new_keys.append(k[0])
        new_products = SanPham.objects.filter(pk__in=new_keys)
        products_images = []
        for new_product in new_products:
            products_images.append(get_Item_By_O(new_product))
        types.insert(0, {'name': 'Sảm phẩm mới nhất', 'products_images': products_images})
        name = get_name(request)
        carts, total = displayCart(request.session.get('carts', ""))
        return render(request, 'site/pages/index.html', {'types': types, 'menu': 'home', 'name_user':name, 'carts': carts, 'total': convertCurrency(total), 'amount': len(request.session.get('carts', []))})

# chuyển hướng đến trang chính sách 
class Delivery(View):
    def get(self, request):
        name = get_name(request)
        carts, total = displayCart(request.session.get('carts', ""))
        return render(request, 'site/pages/chinh-sach.html', {'menu': 'delivery', 'name_user':name, 'carts': carts, 'total': convertCurrency(total), 'amount': len(request.session.get('carts', []))})

# chuyển đến trang liên hệ hoặc lưu thông tin vào database
def Contact(request):
    if request.method == "POST":
        contact = LienHe()
        contact.NoiDung = request.POST.get('NoiDung', "")
        contact.SDT = request.POST.get('SDT', "")
        contact.HoTen = request.POST.get('HoTen', "")
        contact.Email = request.POST.get('Email', "")
        contact.save()
        return redirect('home')
    else:
        name = get_name(request)
        carts, total = displayCart(request.session.get('carts', ""))
        return render(request, 'site/pages/lien-he.html', {'menu': 'contact', 'name_user':name, 'carts': carts, 'total': convertCurrency(total), 'amount': len(request.session.get('carts', []))})

# Chuyển hướng đến trang login
class Login(View):
    def get(self, request):
        return render(request, 'site/pages/login.html')

#Chuyển hướng đến trang đăng kí
class Register(View):
    def get(self, request):
        return render(request, 'site/pages/signup.html')

#Chuyển hướng đến trang quên mật khẩu
class Forget(View):
    def get(self, request):
        return render(request, 'site/pages/forget.html')

#hàm bổ trợ 
# lấy tên người dùng
def get_name(request):
    return request.session.get('name', "")

#hàm bổ trợ 
# lấy username
def get_username(request):
    return request.session.get('username', "")

#hàm bổ trợ 
# chuyển sản phẩm sang dict
def convertToObject(sanpham: SanPham):
    sp = {}
    sp['MaSP'] = sanpham.MaSP
    sp['TenSP'] = sanpham.TenSP
    sp['Gia'] = sanpham.Gia
    return sp

#hàm bổ trợ 
#tính tổng carts
def totalCart(carts):
    total = 0
    for cart in carts:
        total += cart['amount'] * cart['price_sale']
    return total

# chuyển đổi carts trong session thành dạng display để show phía client
def displayCart(carts):
    length = len(carts)
    total = 0
    totalProduct = 0
    for i in range(length):
        totalProduct = carts[i]['amount'] * carts[i]['price_sale']
        total += totalProduct
        carts[i]['total'] = convertCurrency(totalProduct)
        carts[i]['price_sale'] = convertCurrency(carts[i]['price_sale'])
    return carts, total

# ajax lấy huyện từ tỉnh
@csrf_exempt
def getDistricts(request):
    province = request.POST.get('province', "")
    price = Tinh.objects.filter(MaTinh__exact=province).first().MaKV.Gia
    if province != "":
        districts = list(Huyen.objects.filter(MaTinh__MaTinh__exact=province).values_list('MaHuyen', 'TenHuyen'))
        return JsonResponse({'districts': districts, 'price': price, 'totalAll': totalCart(request.session.get('carts', ""))})
    return JsonResponse({})

# ajax lấy xã từ huyện
@csrf_exempt
def getWards(request):
    district = request.POST.get('district', "")
    if district != "":
        wards = list(Xa.objects.filter(MaHuyen__MaHuyen__exact=district).values_list('MaXa', 'TenXa'))
        return JsonResponse({'wards': wards})
    return JsonResponse({})

# ajax thêm sản phẩm khỏi cart
@csrf_exempt
def addCart(request):
    id_product = request.POST['MaSP']
    product_image = get_Item(id_product)
    product_image['product'] = convertToObject(product_image['product'])
    product_image['price_sale'] = int("".join(product_image['price_sale'].split(",")))
    amount_product = int(request.POST['amount'])
    totolProduct = amount_product * product_image['price_sale']
    # Đưa sản phẩm vào Carts
    carts = request.session.get('carts', [])
    exist = False
    length = len(carts)
    amount = length
    for i in range(length):
        if carts[i]['product']['MaSP'] == product_image['product']['MaSP']:
            carts[i]['amount'] = amount_product
            exist = True
            product_image = ""
            break
    if not exist:
        amount += 1
        product_image['amount'] = amount_product
        carts.append(product_image)
    request.session['carts'] = carts

    return JsonResponse({'product_image': product_image, 'totalAll': totalCart(carts), 'totalProduct': totolProduct, 'amount': amount})

# ajax xoá sản phẩm khỏi cart
@csrf_exempt
def deleteCart(request):
    id_product = request.POST['MaSP']
    # Đưa sản phẩm vào Carts
    carts = request.session.get('carts', [])
    length = len(carts)
    amount = length
    for i in range(length):
        if carts[i]['product']['MaSP'] == id_product:
            amount -= 1
            del carts[i]
            break
    request.session['carts'] = carts

    return JsonResponse({'amount': amount, 'totalAll': totalCart(carts)})

# ajax kiểm tra mật khẩu
@csrf_exempt
def checkPassword(request):
    username = request.session.get('username', "")
    password = request.POST.get('password', "")
    if username != "" and password != "":
        rs = KhachHang.objects.filter(MaKH__exact=username, Pass__exact=password).count()
        if rs == 1:
            return JsonResponse({'result_check_pass': True})
    return JsonResponse({'result_check_pass': False})