from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "введите имя"}))
    second_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': "введите фамилию"
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "you@example.com"}))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': "Регион, нас.пункт, улица, дом, квартира"
    }))

    class Meta:
        model = Order
        fields = ('first_name', 'second_name', 'email', 'address')
