from django import forms
from .models import Order
from .constants import PAYMENT_CHOISES, DELIVERY_CHOISES




class QuickOrderForm(forms.Form):
    name = forms.CharField(max_length=50, label="Имя")
    last_name = forms.CharField(max_length=50, label="Фамилия")
    email = forms.EmailField(label="Эл.почта")
    phone = forms.CharField(max_length=50, label="Телефон")
    payment = forms.ChoiceField(choices=PAYMENT_CHOISES, label='Способ оплаты')
    delivery = forms.ChoiceField(choices=DELIVERY_CHOISES, label='Способ Доставки')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('name', 'last_name', 'email', 'phone')