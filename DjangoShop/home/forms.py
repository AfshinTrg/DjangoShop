from django import forms
from .models import Category, Product


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=9)


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ()


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()
