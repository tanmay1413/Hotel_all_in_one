from django import forms
from all_in_one.models import menu

class addProductForm(forms.ModelForm):
    class Meta:
        model = menu
        feilds = ['name','description','category', 'price']
        exclude = ['image']
        