from django.urls import path
from .views import MyAccount, MyOrders, MyAddress, Signup, Forget, Login, Logout, EditInfo, EditAddress, DetailOrder, getOrder, addComment, getMoreComment

urlpatterns = [
    path('addcomment', addComment, name='addcomment'),
    path('morecomment', getMoreComment, name='morecomment'),
    path('info', MyAccount.as_view(), name='myaccount.info'),
    path('orders', MyOrders.as_view(), name='myaccount.orders'),
    path('address', MyAddress.as_view(), name='myaccount.address'),
    path('getorder', getOrder, name='myaccount.getorder'),
    path('login', Login, name='myaccount.login'),
    path('forget', Forget, name='myaccount.forget'),
    path('signup', Signup, name='myaccount.signup'),
    path('logout', Logout, name='myaccount.logout'),
    path('editinfo', EditInfo, name='myaccount.editinfo'),
    path('editaddress', EditAddress, name='myaccount.editaddress'),
    path('detailorder/<str:id_order>/<int:index>', DetailOrder, name='myaccount.detailorder'),
]