from django import forms
from .models import Category, Product


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=9)


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ()


class UpdateCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        exclude = ('sub_category', 'is_sub')


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('category', 'image')









