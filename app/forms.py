from django import forms
from .models import Category, Product

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('slug', 'created', 'update')

        labels ={
            'category':'Категория',
            'description': 'Описание',
            'image': 'Изображение',
            'available': "Доступность товара",
            'price': 'Цена',
        }