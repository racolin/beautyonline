visual studio code
python: 3.9.3
django 3.2
thực hiện lần lượt các bước
1. vào mysql tạo database với <db_name>
2. vào project mở file beautyshop->settings.py->dòng 84 đến 86 sửa theo máy của mình và <db_name> vừa tạo, hoặc cấu hình theo vậy luôn cho đồng bộ. dòng 145, 146 là email của shop để gửi mail cho các tài khoản
3. mở terminal lên 
4. python manage.py makemigrations
5. python manage.py migrate(sau khi thực hiện django tự tạo bảng trong mysql)
6. vào mysql đổ data vào các bảng đó. với cái file data đã up ở trên(chỉ lấy data của các bảng đổ vô)
7. python manage.py runserver
8. vào trình duyệt gõ 127:..../site/home(nhớ là có /site/home) ở dưới terminal có hiện click vô đó cũng đc
9. python manage.py collectstatic để load css, js...
Một số lỗi:
ModuleNotFoundError: No module named 'MySQLdb': thiếu mysql-django, install bằng pip install django-mysql, pip install mysqlclient
