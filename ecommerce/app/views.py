from django.shortcuts import render
from django.http import HttpRequest 
from django.views import View
from .models import Product
from django.db.models import Count

# Create your views here.
def home(request):
    return render(request,'app/home.html')
class CatagoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(catagory=val)
        title = Product.objects.filter(catagory=val).values('title').annotate(total=Count("title"))
        return render(request, "app/catagory.html", locals())
class CatagoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        
        return render(request, "app/catagory.html", locals())

class ProductDetail(View):
    def get(self, request,pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html", locals())