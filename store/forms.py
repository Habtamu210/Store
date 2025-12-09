from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'name', 'category', 'brand', 'description',
            'quantity', 'unit_price'
        ]

