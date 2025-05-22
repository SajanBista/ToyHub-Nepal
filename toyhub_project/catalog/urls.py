from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import register_view, add_to_cart

#app_name = 'catalog'


urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('search/', views.search_view, name='search'),
    path('register/', register_view, name='register'),
    path('buy/', views.buy_cart, name='buy_cart'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='catalog/login.html'), name='login'),
    path('order-success/', views.order_success, name='order_success'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.cart_checkout, name='cart_checkout'),


]
