from django.shortcuts import render
from .models import Product
from django.http import HttpResponse
from django.http import HttpResponse

# Create your views here.
def ft_try(request):
    product = Product.objects.get(pk=1)
    # contet = {
    #     "test": product,
    # }
    return render(request, "myapp/ft_try.html", {"ok" : product})
    #return HttpResponse(product)