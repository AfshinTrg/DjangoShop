from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Category, Product
from .forms import AddToCartForm
from django.contrib.auth.mixins import LoginRequiredMixin
from mixins import AdminRequiredMixin


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, self.template_name, {'products': products, 'categories': categories})


class ProductDetailView(View):
    template_name = 'home/detail.html'
    form_class = AddToCartForm

    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        return render(request, self.template_name, {'product': product, 'form': self.form_class})


class PanelView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'home/panel.html')


class CategoriesListView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'home/category_list.html'

    def get(self, request):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})
