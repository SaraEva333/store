from django.urls import path
from . import views
urlpatterns = [
    path('', views.store_home, name='store_home'),
    path('create', views.create, name='create'),
    path('<int:pk>', views.SDV.as_view(), name='store-detail'),
    path('<int:pk>/update', views.SUV.as_view(), name='store-update'),
    path('<int:pk>/delete', views.SDelV.as_view(), name='store-delete'),
    path('accounts/login/',views.LoginView.as_view(), name="login"),
    path(r'^accounts/register/$', views.RegisterView.as_view(), name="register"),
    path('accounts/<int:pk>/lk', views.lk.as_view(), name='lk'),
    path('accounts/logout', views.LogoutView.as_view(), name='logout'),

    path('add/<int:product_id>', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('cart', views.cart_detail, name='Cart'),

    path(r'^create/', views.order_create, name='order_create'),
    path('orders', views.orders_check, name='orders_check'),
]