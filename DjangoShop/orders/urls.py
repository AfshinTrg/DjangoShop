from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>', views.AddToCartView.as_view(), name='add_cart'),
    path('cart/remove/<int:product_id>', views.RemoveFromCartView.as_view(), name='remove_cart'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('detail/<int:order_id>', views.OrderDetailView.as_view(), name='order_detail'),

]
