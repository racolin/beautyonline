from django.urls import path, include
from .views import Home, Delivery, Contact, Login, Register, Forget, Order, addCart, deleteCart, checkPassword, getDistricts, getWards

urlpatterns = [
    path('order', Order.as_view(), name='order'),
    path('home', Home.as_view(), name='home'),
    path('type/', include('product.urls')),
    path('delivery', Delivery.as_view(), name='delivery'),
    path('contact', Contact, name='contact'),
    path('myaccount/', include('myaccount.urls')),
    path('login', Login.as_view(), name='login'),
    path('signup', Register.as_view(), name='signup'),
    path('forget', Forget.as_view(), name='forget'),
    path('ajax/addcart', addCart, name='addcart'),
    path('ajax/deletecart', deleteCart, name='deletecart'),
    path('ajax/checkpassword', checkPassword, name='checkpassword'),
    path('ajax/districts', getDistricts, name='getdistricts'),
    path('ajax/wards', getWards, name='getwards'),
]