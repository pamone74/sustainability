from django.shortcuts import render
from .models import Manufacturer, Product
from django.http import HttpResponse
from django.http import HttpResponse
from .forms import NameForm
from myapp import views

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

#view functions
def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

def accomodation(request):
    return render(request, 'accomodation.html', {})

def blog_single(request):
    return render(request, 'blog-single.html', {})

def blog(request):
    return render(request, 'blog.html', {})

def contact(request):
    return render(request, 'contact.html', {})

def gallery(request):
    return render(request, 'gallery.html', {})

def elements(request):
    return render(request, 'elements.html', {})