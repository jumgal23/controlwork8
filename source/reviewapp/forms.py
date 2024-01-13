from django import forms
from .models import Products, Reviews


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'category', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'custom-file-input'})


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['product', 'description', 'rating', 'is_moderated']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'moderated': forms.HiddenInput(),
        }

