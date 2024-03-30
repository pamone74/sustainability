from django.shortcuts import render
from .models import Manufacturer, Product, ProfileUser
from django.http import HttpResponse, HttpResponseRedirect
from .forms import NameForm, ProductForm, EventForm, RegistrationForm, ProfileForm
from django.views import View
from django.contrib import messages
from datetime import date

#Amone's views 
def get_date():
    return datetime.datetime.now()

def add_product(request):
    submitted = False
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/add_product/?submitted=True")
    else:
        form = ProductForm()
        if "submitted" in request.GET:
            submitted = True
    return render(request, "myapp/add_product.html", {"form": form, "submitted": submitted})    

def get_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, "myapp/detail.html", {"product": product})

def reuse(request):
    objects = Product.objects.all()
    return render(request, "myapp/reuse.html", {"product": objects})

def search_result(request):
    if request.method == "POST":
        searched = request.POST['searched']
        product = Product.objects.filter(product_name__contains=searched)
        return render(request, "myapp/search_result.html", {"searched": searched, "product": product})
    else:
        return render(request, "myapp/search_result.html", {})

def update(request,pk):
    obj = Product.objects.get(pk=pk)
    form = ProductForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/reuse/")
    return render(request, "myapp/update.html", {"object":obj, "form":form})

def add_event(request):
   if request.method == "POST":
         form = EventForm(request.POST)
         if form.is_valid():
              form.save()
              return HttpResponseRedirect("/add_event/")

def recycle(request):
    product = Product.objects.all()
    return render(request, "myapp/recycle.html", {"product": product})


class Registration(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "register.html", locals())
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful")
            # return HttpResponseRedirect("login/")
        else:
            messages.warning(request, "Invalid Data")
        return render(request, "register.html", locals())


class Profileview(View):
    def get(self, request):
      form = ProfileForm()
      return render(request, "create_profile.html", locals())
    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data["full_name"]
            city = form.cleaned_data["city"]
            address = form.cleaned_data["address"]
            phone = form.cleaned_data["phone"]
            country_progin = form.cleaned_data["country_origin"]
            country = "UAE"
            email = request.user.email
            reg_date = date.today()
            reg = ProfileUser(user=user, full_name=name,address=address,city=city, phone=phone, date_created=reg_date,date_updated=reg_date, country=country, country_origin=country_progin, email=email)
            reg.save()
            messages.success(request, "Profile Updated")
            return HttpResponseRedirect("/information/")
        else:
            messages.warning(request, "Invalid Data")
        return render(request, "profile.html", locals())



def Information(request):
    info = ProfileUser.objects.filter(user=request.user)
    return render(request, "information.html", locals())

# This is a dummy view function just as a placeholder for the dashboard urls
def Dummy(request):
    return render(request, "dummy.html")

def Analytics(request):
    return render(request, "dashboard.html")
# Allan's view functions

def home(request):
    return render(request, 'index.html', {})

def dashboard(request):
    return render(request, 'dashboard.html', {})

class UpdateInformation(View):
    def get(self, request, pk):
        obj = ProfileUser.objects.get(pk=pk)
        form = ProfileForm(instance=obj)
        return render(request, "update.html", locals())
    def post(self, request, pk):
        obj = ProfileUser.objects.get(pk=pk)
        form = ProfileForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated")
            return HttpResponseRedirect("/information/")
        else:
            messages.warning(request, "Invalid Data")
        return render(request, "update.html", locals())
def Dashboard(request):
    form = ProfileForm()
    return render(request, "profile.html", locals())

def dashboard(request):
    form = ProfileForm()
    return render(request, "dashboard.html", locals())