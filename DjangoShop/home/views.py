from django.shortcuts import render
from django.views import View
from .models import Category, Product


class HomeView(View):

    def get(self, request):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        return render(request, 'home/home.html', {'products': products, 'categories': categories})


