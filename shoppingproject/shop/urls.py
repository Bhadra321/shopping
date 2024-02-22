from  . import views
from django.urls import path
app_name = 'shop'

urlpatterns = [
    path('',views.allprodcat,name='allprodcat'),
    path('shop/<slug:c_slug>/',views.allprodcat,name='products_by_category'),
    path('shop/<slug:c_slug>/<slug:product_slug>/',views.proDetail,name='prodcatdetail'),
    path('search/', views.SearchResuls, name='SearchResults'),
    path('add/<int:product_id>',views.add_cart,name='add_cart'),
    path('cart/',views.cart_detail,name='cart_detail'),
    path('remove/<int:product_id>/',views.cart_remove,name='cart_remove'),
    path('full_remove/<int:product_id>/',views.full_remove,name='full_remove'),



]