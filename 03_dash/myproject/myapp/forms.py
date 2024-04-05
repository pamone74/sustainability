from django import forms
from django.forms import ModelForm
from .models import Product,AddEvent, ProfileUser, ReuseProducts,Ownership
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
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
        fields = ["product_name","product_quantity","manufacturer_name","manufacture_location","product_type","product_mf_date",
                  "product_expiry_date",]
        widgets = {
            "product_name": forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter Product Name"}),
            "manufacturer_name": forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter Manufacturer Name"}),
            "manufacture_location": forms.Select(attrs={"class":"form-control", "placeholder":"Enter Manufacture Location"}), 
            "product_type": forms.Select(attrs={"class":"form-control", "placeholder":"Enter Product Type"}),
            "product_mf_date": forms.DateInput(attrs={"class":"form-control", "placeholder":"Enter Manufacturing Date"}),
            "product_quantity": forms.NumberInput(attrs={"class":"form-control", "placeholder":"Enter Product Quantity"}),
            "product_expiry_date": forms.DateInput(attrs={"class":"form-control", "placeholder":"Enter Expiry Date"}),
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
        fields = ['username','ID_number', 'password1', 'password2', 'email']

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
        fields = ['full_name','address', 'phone', 'city', 'country_origin',"user_type"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter Full Name"}),
            "address": forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter Address"}),
            "phone": forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter Phone Number"}),
            "city": forms.Select(attrs={"class":"form-control", "placeholder":"Enter City"}),
            "country_origin": forms.Select(attrs={"class":"form-control", "placeholder":"Enter Country Origin"}),
            "user_type": forms.Select(attrs={"class":"form-control", "placeholder":"Enter User Type"}),
        }


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'Old Password','class':'form-control',
    }))
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'New Password','class':'form-control',
    }))
    new_password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password','class':'form-control',
    }))
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


#  Password Reset

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control',
    }))
    
class MySetPasswordForm(SetPasswordForm):
        new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={
            'placeholder': 'New Password',
            'class': 'form-control',
        }))
        new_password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control',
        }))
        class Meta:
            model = User
            fields = ['new_password1', 'new_password2']

class ReuseProductForm(ModelForm):
    class Meta:
        model = ReuseProducts
        fields = ['product_name', 'product_catagories', 'product_condition', 'product_quantity', 'product_image','product_description', 'product_address']
        widgets = {
            "product_name": forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter Product Name"}),
            "product_quantity": forms.NumberInput(attrs={"class":"form-control", "placeholder":"Enter Product Quantity"}),
            "product_catagories": forms.Select(attrs={"class":"form-control", "placeholder":"Enter Product Catagories"}),
            "product_condition": forms.Select(attrs={"class":"form-control", "placeholder":"Enter Product Condition"}),
            "product_image": forms.FileInput(attrs={"class":"form-control", "placeholder":"Enter Product Image"}),
            "product_description": forms.Textarea(attrs={"class":"form-control", "placeholder":"Enter Product Description"}),
            "product_address": forms.Textarea(attrs={"class":"form-control", "placeholder":"Enter Product Address"}),
        }


class TransferOwnershipForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        user = ProfileUser.objects.get(user=user)
        super().__init__(*args, **kwargs)
        if user:
            # Filter queryset of product field based on current user
            self.fields['product'].queryset = Product.objects.filter(product_ownership=user)
    class Meta:
        model = Ownership
        fields = ['new_owner','product', 'product_quantity', 'status',]
        widgets = {
            "product": forms.Select(attrs={"class":"form-control", "placeholder":"Enter Product"}),
            "product_quantity": forms.NumberInput(attrs={"class":"form-control", "placeholder":"Enter Product Quantity"}),
            "status": forms.Select(attrs={"class":"form-control", "placeholder":"Enter Status"}),
            "new_owner": forms.Select(attrs={"class":"form-control", "placeholder":"Enter New Owner"}), 
        }


class SmartDustBinForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter userame"}))
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Location"}))
    product_code = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Product Code"}))
    product_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Product Name"}))


    def clean_name(self):
        name = self.cleaned_data.get('name')
        try:
            User.objects.get(username=name)
        except User.DoesNotExist:
            raise forms.ValidationError("User Does not exists")
        return name