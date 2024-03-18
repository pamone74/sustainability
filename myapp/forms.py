from django import forms
from django.forms import ModelForm
from .models import Manufacturer, Product

class NameForm(forms.Form):
    your_name = forms.CharField(label="Name",max_length=100)
    your_email = forms.EmailField(label="Email",max_length=100)
    your_age = forms.IntegerField(label="Age",max_value=100)
    your_password = forms.CharField(label="Password",max_length=100,widget=forms.PasswordInput) 
    your_password_confirm = forms.CharField(label="Confirm Password",max_length=100,widget=forms.PasswordInput)

#create a  class
    
class ManufacturerForm(ModelForm):
    class Meta:
        model = Manufacturer
        fields = "__all__"

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
    
 