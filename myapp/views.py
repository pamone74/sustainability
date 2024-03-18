from django.shortcuts import render
from .models import Manufacturer, Product
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from .forms import NameForm, ManufacturerForm, ProductForm

# Create your views here.
def ft_try(request):
    return render(request,"myapp/index.html",{})

def get_name(request):
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.isvalid():
            return HttpResponseRedirect("/thanks/")
    else:
        form = NameForm()
    
    return render(request, "myapp/name.html", {"form": form})
