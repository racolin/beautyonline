from django.core import paginator
from django.shortcuts import render, redirect
from django.views import View
from .models import Comment, SanPham, AnhSanPham, LoaiSanPham, KhoangGia, GiamGia, SapXep
from myaccount.models import ChiTietHoaDon, HoaDon
from core.support import convertCurrency
from datetime import datetime, timedelta
from django.db.models import Count, Q
from core.support import displayCart
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

# hiển thị cho Item
class Item(View):
    def get(self, request, *args, **kwargs):
        id_product = kwargs.get('id_product', "")
        mode = kwargs.get('mode', "")
        content = get_Item_Detail(id_product)
        content['id_product'] = id_product
        content['types'] = get_all_types()
        content['price_ranges'] = get_price_range()
        category = content['product'].MaLSP
        content['category'] = category
        content['menu'] = mode
        content['related_products'] = get_ralated_product(content['product'])
        content['name_user'] = get_name(request)
        carts, total = displayCart(request.session.get('carts', ""))
        content['carts'] = carts
        content['total'] = convertCurrency(total)
        content['amount'] = len(request.session.get('carts', []))
        content['current_comment'], content['still'], content['comments'] = getCommemt(id_product, 0)
        content['average'] = getRate(id_product)
        return render(request, 'site/pages/chi-tiet-san-pham.html', content)
   
# Hiển thị cho danh mục
class Category(View):
    def get(self, request, *args, **kwargs):
        mode = kwargs.get('mode', "")
        if mode not in ['product', 'sale', 'selling']:
            return redirect('home')
        id_category = kwargs.get('id_category', "")
        id_filter = kwargs.get('id_filter', "")
        id_sort = kwargs.get('id_sort', "")
        
        page_choose = 1
        try:
            page_choose = int(request.GET.get('page', '1'))
        except ValueError:
            page_choose = 1
        content = addCategory(mode, id_category, id_filter, id_sort, page_choose)
    
        content['types'] = get_all_types()
        content['price_ranges'] = get_price_range()
        content['name_user'] = get_name(request)
        content['id_filter'] = id_filter
        content['id_sort'] = id_sort
        content['list_sort'] = get_all_sort()

        carts, total = displayCart(request.session.get('carts', ""))
        content['carts'] = carts
        content['total'] = convertCurrency(total)
        content['menu'] = mode
        content['amount'] = len(request.session.get('carts', []))
        return render(request, 'site/pages/san-pham.html', content) 

# lấy về nội dung của tất cả các sản phẩm được lọc
# lọc theo mode:[product, sale, selling] category, filter, sort
def addCategory(mode, id_category, id_filter, id_sort, page_choose):
    content = {}
    products = []

    if mode == 'product':
        #
        products = []
        if id_category == 'all':
            content['category'] = {'MaLSP': 'all', 'TenLSP': 'Tất cả sản phẩm'}
            products = SanPham.objects.all()
        else:
            loai = LoaiSanPham.objects.filter(MaLSP__exact=id_category).first()
            content['category'] = {'MaLSP': loai.MaLSP, 'TenLSP': loai.TenLSP}
            products = SanPham.objects.filter(MaLSP__exact=id_category)
        #
    if mode == 'selling':
        #
        temp = HoaDon.objects.filter(NgayDatHang__gte=datetime.now() - timedelta(days=60)).values('MaHD')
        hoadon = []
        for tem in temp:
            hoadon.append(tem['MaHD'])
        cthds = []

        if id_category == 'all':
            content['category'] = {'MaLSP': 'all', 'TenLSP': 'Tất cả sản phẩm'}
            cthds = ChiTietHoaDon.objects.filter(MaHD__in=hoadon).values('MaSP').annotate(TongSL=Count('SoLuong')).order_by('-TongSL')
        else:
            loai = LoaiSanPham.objects.filter(MaLSP__exact=id_category).first()
            content['category'] = {'MaLSP': loai.MaLSP, 'TenLSP': loai.TenLSP}
            cthds = ChiTietHoaDon.objects.filter(MaHD__in=hoadon, MaSP__MaLSP__MaLSP__exact=id_category).values('MaSP').annotate(TongSL=Count('SoLuong')).order_by('-TongSL')
        
        id_products = []
        for cthd in cthds:
            id_products.append(cthd['MaSP'])
        products = SanPham.objects.filter(MaSP__in=id_products)
        #
    if mode == 'sale':
        #
        sales = []
        if id_category == 'all':
            content['category'] = {'MaLSP': 'all', 'TenLSP': 'Tất cả sản phẩm'}
            sales = GiamGia.objects.filter(NgayKetThuc__gte=datetime.now())
        else:
            loai = LoaiSanPham.objects.filter(MaLSP__exact=id_category).first()
            content['category'] = {'MaLSP': loai.MaLSP, 'TenLSP': loai.TenLSP}
            sales = GiamGia.objects.filter(NgayKetThuc__gte=datetime.now(), MaSP__MaLSP__MaLSP__exact=id_category).values('MaSP')

        id_products = []
        for sale in sales:
            id_products.append(sale.MaSP.MaSP)
        
        products = SanPham.objects.filter(MaSP__in=id_products)
        # 
      
    products = filter_price(products, id_filter)

    products = sort(products, id_sort)       

    paginator = Paginator(products, 9)

    num_pages = paginator.num_pages
    if page_choose > num_pages:
        page_choose = num_pages
    try:
        products = paginator.page(page_choose)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    products_images = []
    for product in products:
        products_images.append(get_Item_By_O(product))
    content['products_images'] = products_images
    content['page_range'] = paginator.page_range
    content['page_current'] = page_choose
    content['page_after'] = num_pages if page_choose + 1 > num_pages else page_choose + 1
    content['page_before'] = 1 if page_choose - 1 < 1 else page_choose - 1
    content['num_pages'] = num_pages
    return content

# lọc các sản phẩm nằm trong khoảng giá có MaKG = id_filter
# nếu id_filter rỗng thì trả lại products
def filter_price(products, id_filter):
    if id_filter != "":
        fil = KhoangGia.objects.filter(MaKG__exact=id_filter).first()
        min_price = fil.Gia_Min
        max_price = fil.Gia_Max
        if min_price == max_price:
            return products.filter(Gia__gte=min_price)
        else:
            return products.filter(Gia__gte=min_price, Gia__lt=max_price)
    return products

# sắp xếp các sản phẩm theo MaSX = id_sort
# nếu id_sort rỗng thì trả lại products
def sort(products, id_sort):
    if id_sort != "":
        return products.order_by(id_sort) 
    return products

# lấy info sản phẩm và tất cả các ảnh của nó và ảnh nổi bật
def get_Item_Detail(id_product):
    product = SanPham.objects.filter(MaSP__exact=id_product).first()
    images = AnhSanPham.objects.filter(MaSP__exact=product.MaSP).order_by('-LoaiAnh')
    content = get_Item_By_O(product)
    content['images'] = images
    return content

# lấy info sản phẩm và ảnh nổi bật của nó
def get_Item(id_product):
    product = SanPham.objects.filter(MaSP__exact=id_product).first()
    return get_Item_By_O(product)

# lấy tất cả các loại sản phẩm
def get_all_types():
    types = [{'MaLSP': 'all', 'TenLSP': 'Tất cả sản phẩm'}]
    loai = LoaiSanPham.objects.values_list('MaLSP', 'TenLSP')
    for l in loai:
        types.append({'MaLSP': l[0], 'TenLSP': l[1]})
    return types

# lấy khoảng giá 
def get_price_range():
    price_range = []
    r_rs = KhoangGia.objects.values_list('MaKG', 'Gia_Min', 'Gia_Max')
    for r_r in r_rs:
        price = ''
        if r_r[1] == 0:
            price = 'Giá dưới ' + convertCurrency(r_r[2]) + 'đ'
        elif r_r[2] == r_r[1]:
            price = 'Giá trên ' + convertCurrency(r_r[2]) + 'đ'
        else:
            price = convertCurrency(r_r[1]) + 'đ ' + '- ' + convertCurrency(r_r[2]) + 'đ'
        price_range.append({'Ma': r_r[0], 'price': price})
    return price_range

# lấy các sản phẩm liên quan đến 1 product
def get_ralated_product(product: SanPham):
    price = int("".join(product.Gia.split(',')))
    max_price = price + 50000
    min_price = 0 if price - 50000 < 0 else price - 50000
    brand = product.MaTH
    types = product.MaLSP
    products = SanPham.objects.filter(Q(Gia__gte=min_price) & Q(Gia__lte=max_price) | Q(MaTH=brand) | Q(MaLSP=types)).distinct()
    content = []
    for product in products:
        content.append(get_Item_By_O(product))
    return content

# lấy thông tin gồm ảnh và giá của nó khi đã giảm
def get_Item_By_O(product: SanPham):
    images = AnhSanPham.objects.filter(MaSP__exact=product.MaSP).order_by('-LoaiAnh')
    image_main = images.first()
    price_sale = GiamGia.objects.filter(MaSP__exact=product.MaSP, NgayKetThuc__gt=datetime.now()).first()
    price_rate = price_sale.PhanTram if price_sale else 0
    price_sale = convertCurrency(int((1 - price_rate) * product.Gia ))
    product.Gia = convertCurrency(product.Gia)
    return {'product': product,'image': image_main.NguonAnh, 'price_sale': price_sale}

# lấy tên người dùng tại session nếu chưa đăng nhập thì rỗng
def get_name(request):
    return request.session.get('name', "")

# lấy tất cả các kiểu sắp xếp có trong database
def get_all_sort():
    return SapXep.objects.all()

def getRate(id_product):
    comments = Comment.objects.filter(MaSP__MaSP__exact=id_product)
    total = 0
    count = 0
    for comment in comments:
        count += 1
        total += comment.Rate
    return total / count if count != 0 else 0

def getCommemt(id_product, fom):
    comments = Comment.objects.filter(MaSP__MaSP__exact=id_product).order_by('-ThoiGian')[fom:fom+3]
    content = []
    for comment in comments:
        content.append({'TenKH': comment.MaKH.TenKH, 'rate': comment.Rate, 'ThoiGian': comment.ThoiGian, 'ChiTiet': comment.ChiTietCM})
    return fom + 3, comments.count() == 3, content

