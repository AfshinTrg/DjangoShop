from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Category, Product
from orders.models import Order, OrderItem
from .forms import AddToCartForm, AddCategoryForm, AddProductForm, UpdateCategoryForm, UpdateProductForm
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
        categories = Category.objects.filter(is_sub=False)
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


class UpdateCategoryView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'home/update_category.html'
    form_class = UpdateCategoryForm

    def setup(self, request, *args, **kwargs):
        self.category_instance = get_object_or_404(Category, pk=kwargs['category_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        category = self.category_instance
        form = self.form_class(instance=category)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        category = self.category_instance
        form = self.form_class(request.POST, instance=category)
        if form.is_valid():
            form.save()
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


class RemoveProductView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        product.delete()
        return redirect('home:products_list')


class UpdateProductView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'home/update_category.html'
    form_class = UpdateProductForm

    def setup(self, request, *args, **kwargs):
        self.product_instance = get_object_or_404(Product, pk=kwargs['product_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product = self.product_instance
        form = self.form_class(instance=product)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        product = self.product_instance
        form = self.form_class(request.POST, instance=product)
        if form.is_valid():
            form.save()
        return redirect('home:products_list')


class OrdersListView(LoginRequiredMixin, View):
    template_name = 'home/orders_list.html'

    def get(self, request):
        if request.user.is_superuser:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=request.user)
        return render(request, self.template_name, {'orders': orders})


class OrdersDetailView(LoginRequiredMixin, View):
    template_name = 'home/order_detail.html'

    def get(self, request, order_id):
        if request.user.is_superuser:
            order = get_object_or_404(Order, pk=order_id)
        else:
            order = get_object_or_404(Order, pk=order_id, user=request.user)
        total_price = order.get_total_price()
        order_item = OrderItem.objects.filter(order=order_id)
        return render(request, self.template_name, {'order_item': order_item, 'total_price': total_price})













