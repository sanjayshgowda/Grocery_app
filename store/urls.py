from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # For built-in authentication views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-products/', views.manage_products, name='manage_products'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-category/', views.add_category, name='add_category'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
]
