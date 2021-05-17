visual studio code
python: 3.9.3
django 3.2
0. vào project mở file beautyshop->settings.py->dòng 84 đến 86 sửa theo máy của mình, hoặc cấu hình theo vậy luôn cho đồng bộ. dòng 145, 146 là email của shop để gửi mail cho các tài khoản
1. mở terminal lên 
2. python manage.py makemigrations
2. python manage.py migrate(sau khi thực hiện django tự tạo bảng trong mysql)
3. vào mysql đổ data vào các bảng đó. với cái file data đã up ở trên(chỉ lấy data của các bảng đổ vô)
4. python manage.py runserver
5. vào trình duyệt gõ 127:.... ở dưới terminal có hiện click vô đó cũng đc
