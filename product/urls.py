from django.urls import path
from .views import Item, Category

urlpatterns = [
    path('<str:mode>/item/<str:id_product>', Item.as_view(), name='mode.item'),
    path('<str:mode>/category/<str:id_category>', Category.as_view(), name='mode.category'),
    path('<str:mode>/category/<str:id_category>/filter/<str:id_filter>', Category.as_view(), name='mode.category.filter'),
    path('<str:mode>/category/<str:id_category>/filter/<str:id_filter>/sort/<str:id_sort>', Category.as_view(), name='mode.category.filter'),
    path('<str:mode>/category/<str:id_category>/sort/<str:id_sort>', Category.as_view(), name='mode.category.filter'),
    path('<str:mode>/category/<str:id_category>/sort/<str:id_sort>/filter/<str:id_filter>', Category.as_view(), name='mode.category.filter'),
]