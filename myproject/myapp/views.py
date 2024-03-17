from django.shortcuts import render
from .models import Manufacturer, Product
from django.http import HttpResponse
from django.http import HttpResponse
from .forms import NameForm

# Create your views here.
def ft_try(request):
    return HttpResponse("Hello, world. You're at the ft_try index.")

def get_name(request):
    if reques.method == "POST":
        form = NameForm(request.Form)
        if form.isvalid():
            return HttpResponseRedirect("/thanks/")
    else:
        form = NameForm()
    
    return render(request, "name.html", {"form": form})