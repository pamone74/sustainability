from django.shortcuts import render
from .models import Manufacturer, Product, Ownership
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from .forms import NameForm, ProductForm, EventForm
import datetime

# Create your views here.
def get_date():
    return datetime.datetime.now()

def ft_try(request):
    return render(request,"myapp/base.html",{})

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