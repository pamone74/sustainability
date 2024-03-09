from django.shortcuts import render
from .models import Manufacturer, Products
from django.http import HttpResponse
from django.http import HttpResponse

# Create your views here.
def ft_try(request):
    product = Manufacturer.objects.get(pk=1)
    # contet = {
    #     "test": product,
    # }
    return render(request, "myapp/ft_try.html", {"ok" : product})
    #return HttpResponse(product)