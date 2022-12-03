from .models import book, Order
from django.forms import ModelForm, TextInput
from django.contrib.auth.models import User
from django import forms

class BookForm(ModelForm):
    class Meta:
        model = book
        fields = ['title','author', 'price','data']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Название книги'
            }),
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Автор книги'
            }),
            'price': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена книги'
            }),
            'data': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Год написания книги'
            }),
        }
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email','first_name']

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Имя пользователя'
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),

            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Логин'
            }),
        }


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)



class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']






