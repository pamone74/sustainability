from django import forms
from django.forms import ModelForm
from .models import Manufacturer, Product,AddEvent, ProfileUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User

#Amone' s form
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
        
class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "class":"form-control", 
        "placeholder":"Enter Username"}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={
        "class":"form-control",
          "placeholder":"Enter Email"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        "class":"form-control",
        "placeholder":"Enter Password"}))
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={
        "class":"form-control", 
        "placeholder":"Confirm Password"}))
    ID_number = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "class":"form-control", 
        "placeholder":"Enter EID Number or Passport"}))

    class Meta:
        model = User
        fields = ['username','ID_number', 'password1', 'password2', 'email',]

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autofocus': 'False',
        'placeholder': 'Username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
    }))

class ProfileForm(ModelForm):
    class Meta:
        model = ProfileUser
        fields = ['full_name','address', 'phone', 'city', 'country_origin']
        widgets = {
            "full_name": forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter Full Name"}),
            "address": forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter Address"}),
            "phone": forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter Phone Number"}),
            "city": forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter City"}),
            "country_origin": forms.Select(attrs={"class":"form-control scrollable-select", "placeholder":"Enter Country Origin"}),
        }
