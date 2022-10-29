from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Category, Product
from .forms import AddToCartForm, AddCategoryForm, AddProductForm
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


class AddCategoryView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'home/add_category.html'
    form_class = AddCategoryForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:category_list')
        return render(request, self.template_name, {'form': form})


class RemoveCategoryView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        category.delete()
        return redirect('home:category_list')


class ProductsListView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'home/products_list.html'

    def get(self, request):
        products = Product.objects.filter(available=True)
        return render(request, self.template_name, {'products': products})


class AddProductView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'home/add_product.html'
    form_class = AddProductForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home:products_list')
        return render(request, self.template_name, {'form': form})







