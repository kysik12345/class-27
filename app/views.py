from django.shortcuts import render
from django.views.generic import (ListView, CreateView, 
                                  UpdateView, DetailView, 
                                  DeleteView, TemplateView)
from .models import Product, Category
from django.urls import reverse_lazy
from .forms import CategoryCreateForm, ProductCreateForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404

class AdminTemplateView(TemplateView):
    template_name='app/admin.html'

class IndexTemplateView(TemplateView):
    template_name = 'app/app.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        # products = Product.objects.all()
        context['categories'] = categories
        # context['products'] = products

        return context

class ProductListByCategory(ListView):
    model = Product
    template_name = 'app/products_by_category.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories

        return context

    def get_queryset(self):
        if not self.kwargs.get('slug'):
            return Product.objects.all
        
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=category)

class ProductCreateView(CreateView):
        model = Product
        form_class = ProductCreateForm
        template_name = 'app/product_add.html'
        success_url = reverse_lazy('products')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'app/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['total'] = 5
    #     return context

class ProductListView(ListView):
    model = Product
    template_name = 'app/app.html'
    context_object_name = 'products'

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'app/product_edit.html'
    context_object_name = 'product'


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'app/product_delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('products')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'app/category_edit.html'
    context_object_name = 'category'


class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    form = CategoryCreateForm
    template_name = 'app/product_add.html'
    success_url = reverse_lazy('categories')

class CategoryListView(ListView):
    model = Category
    template_name = 'app/categories.html'
    context_object_name = 'categories'

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'app/category_delete.html'
    context_object_name = 'category'
    success_url = reverse_lazy('categories')

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'app/category_detail.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'

class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'
    form = CategoryCreateForm
    template_name = 'app/category_add.html'
    success_url = reverse_lazy('categories')

def index(request):
    ads = Category.objects.all().order_by('-created_at')
    paginator= Paginator(ads, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'app/app.html', context)

def product_search(request):
     query = request.GET.get('query')
     query_text = Q(name__icontains = query)

     results = Product.objects.filter(query_text)
     categories = Category.objects.all()
     
     context = {'categories':categories, 'products': results}

     return render (request,template_name="app/app.html", context=context)
