from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>/', views.HomeView.as_view(), name='category_filter'),
    path('product/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]

urlpatterns += [
    path('panel/', views.PanelView.as_view(), name='panel'),
    path('panel/categories/', views.CategoriesListView.as_view(), name='category_list'),
    path('panel/category/add/', views.AddCategoryView.as_view(), name='add_category'),
    path('panel/category/remove/<slug:category_slug>/', views.RemoveCategoryView.as_view(), name='remove_category'),
    path('panel/products/', views.ProductsListView.as_view(), name='products_list'),
    path('panel/product/add/', views.AddProductView.as_view(), name='add_product'),

]
