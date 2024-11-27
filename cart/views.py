
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

from app.models import Product
from project.settings import CART_SESSION_ID
from .models import CartUser, CartItem


class Cart:
    def __init__(self, request):
        # получаем текущую сессию
        self.session = request.session
        # получаем текущего пользователя
        self.user = request.user
        # получаем корзину из сессии или создаем новую
        cart = self.session.get(CART_SESSION_ID)
        # создаем новую корзину
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    # сохранение изменений в сессию
    def save(self):
        self.session.modified = True

    def copy(self):
        return self.cart.copy()

    # метод помещения товара в корзину
    def add(self, product, quantity=1, override_quantity=False):
        # получаем id товара из ОБЪЕКТА товара
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    # удаление товара из корзины
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # метод подсчета общего количества элементов в корзине
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
        # return len(self.cart) - количество товаров в корзмне (без учета кол-ва каждого товара)

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        self.cart.clear()
        # del self.session[CART_SESSION_ID]
        self.save()

    # def prod_id_str(self):
    #     return self.cart[]

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


# корзина авторизованного пользователя
class ProductCartUser:
    def __init__(self, request):
        # получаем текущего пользователя
        self.user = request.user
        # получаем корзину польз-ля из БД или создаем НОВУЮ
        self.user_cart, created = CartUser.objects.get_or_create(user=self.user)
        # получаем позиции товаров в корзине
        products_in_cart = CartItem.objects.filter(cart=self.user_cart)
        # создаем объект для хранения товаров
        self.cart = {}

        for item in products_in_cart:
            self.cart[str(item.product.id)] = {'quantity': item.quantity, 'price': item.product.price}

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    # метод сохранения корзины в БД
    def save(self):
        for prod_id in self.cart:
            product = Product.objects.get(pk=prod_id)
            # проверяем наличие товара в БД
            # если есть - обновляем кол-во
            if CartItem.objects.filter(cart=self.user_cart, product=product).exists():
                item = CartItem.objects.get(cart=self.user_cart, product=product)
                item.quantity = self.cart[prod_id]['quantity']
                item.save()
            # иначе - создаем новую позицию
            else:
                CartItem.objects.create(cart=self.user_cart, product=product, quantity=self.cart[prod_id]['quantity'])

    def remove(self, product_id, request):
        product = Product.objects.get(pk=product_id)
        cart_user = CartUser.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart_user, product=product)
        cart_item.delete()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())


def cart_add(request, slug):
    product = get_object_or_404(Product, slug=slug)
    print(product)
    # создаем корзину (получаем из сессии или БД)
    if request.user.id:
        cart = ProductCartUser(request)
    else:
        cart = Cart(request)
    print(cart)

    cart.add(product=product)
    print(cart.cart)
    return redirect('/')


def cart_detail(request):
    return render(request, template_name='cart/cart_detail.html')


@csrf_exempt
def update_cart_by_front(request):
    data = json.loads(request.body)
    print(data)
    print(type(data))
    product_id = data.get('productIdValue')
    quantity = data.get('quantityValue')

    if product_id:
        if request.user.id:
            cart = ProductCartUser(request)
        else:
            cart = Cart(request)

        product = get_object_or_404(Product, pk=int(product_id))
        cart.add(product=product, quantity=int(quantity), override_quantity=True)
        print('ok', cart.cart)
        response_data = {'result': 'success'}
    else:
        response_data = {'result': 'failed'}

    return JsonResponse(response_data)


def remove_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.user.id:
        cart = ProductCartUser(request)
        cart.remove(product_id, request)
    else:
        cart = Cart(request)
        cart.remove(product)

    return redirect("cart_detail")


@csrf_exempt
def remove_product_ajax(request):
    data = json.loads(request.body)
    product_id = data.get('productIdValue')
    product = get_object_or_404(Product, pk=product_id)
    if request.user.id:
        cart = ProductCartUser(request)
        cart.remove(product_id, request)
    else:
        cart = Cart(request)
        cart.remove(product)

    response_data = {'result': 'success'}
    return JsonResponse(response_data)


def remove_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


def get_cart_length(request):
    cart = Cart(request)
    cart_length = len(cart)
    print(cart_length)
    response_data = {"cart_length": cart_length}
    return JsonResponse(response_data)
