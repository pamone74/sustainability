from django import forms
from django.forms import ModelForm
from .models import Manufacturer, Product,AddEvent

class NameForm(forms.Form):
    your_name = forms.CharField(label="Name",max_length=100)
    your_email = forms.EmailField(label="Email",max_length=100)
    your_age = forms.IntegerField(label="Age",max_value=100)
    your_password = forms.CharField(label="Password",max_length=100,widget=forms.PasswordInput) 
    your_password_confirm = forms.CharField(label="Confirm Password",max_length=100,widget=forms.PasswordInput)

#create a  class

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "product_name": forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter Product Name"}),
            "manufacturer_name": forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter Manufacturer Name"}),
            "manufacture_location": forms.Select(attrs={"class":"form-control", "placeholder":"Enter Manufacture Location"}), 
            "product_type": forms.Select(attrs={"class":"form-control", "placeholder":"Enter Product Type"}),
            "product_quantity": forms.NumberInput(attrs={"class":"form-control", "placeholder":"Enter Product Quantity"}),
            "product_mf_date": forms.DateInput(attrs={"class":"form-control", "placeholder":"Enter Manufacturing Date"}),
            "product_expiry_date": forms.DateInput(attrs={"class":"form-control", "placeholder":"Enter Expiry Date"}),
            "product_ownership": forms.Select(attrs={"class":"form-control", "placeholder":"Enter Ownership"}),
        }
    
class EventForm(ModelForm):
    class Meta:
        model = AddEvent
        fields = '__all__'
        widgets={
            "event_name": forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter Event Name"}),
            "event_location": forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter Event Location"}),
            "event_date": forms.DateInput(attrs={"class":"form-control", "placeholder":"Enter Event Date"}),
            "event_time": forms.TimeInput(attrs={"class":"form-control", "placeholder":"Enter Event Time"}),
            "event_description": forms.Textarea(attrs={"class":"form-control", "placeholder":"Enter Event Description"}),
        }