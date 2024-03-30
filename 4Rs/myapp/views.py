from django.shortcuts import render
from .models import Manufacturer, Product, ProfileUser, ReuseProducts, Cart, Customer
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import NameForm, ProductForm, EventForm, RegistrationForm, ProfileForm, ReuseProductForm
from django.views import View
from django.contrib import messages
from datetime import date
from django.db.models import Q

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


# This is the resue funcion that will be called when the user wants to see the products that are available for reuse
def reuse(request):
    objects = ReuseProducts.objects.all()
    return render(request, "reuse.html", {"product": objects})

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
    return render(request, "profile.html")
# Allan's view functions

def home(request):
    return render(request, 'index.html', {})

def index(request):
    return render(request, 'base_login.html', {})


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

# This function is used to add a product that is available for reuse

class AddResueProduct(View):
    def get(self, request):
        form = ReuseProductForm()
        return render(request, "add_reuse_product.html", locals())
    def post(self, request):
        form = ReuseProductForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            product_save = form.save(commit=False)
            product_save.user = user
            product_save.save()
            messages.success(request, "Product Added")
            return HttpResponseRedirect("/reuse/")
        else:
            messages.warning(request, "Invalid Data")
        return render(request, "add_reuse_product.html", locals())

# This function is used to search for a product
# it should return the product that is being searched for
    

def search_result(request):
    if request.method == "POST":
        searched = request.POST['searched']
        product = ReuseProducts.objects.filter(product_name__contains=searched)
        return render(request, "search_result.html", locals())
    else:
        return render(request, "myapp/search_result.html", {})


# This function is used to add a product to the cart
# it should return the product that is being added to the cart
# Then it should redirect to the cart page
def add_product_to_cart(request):
    user = request.user
    product_id = request.GET.get("pro_id")[:-1]
    product = ReuseProducts.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return HttpResponseRedirect("/cart/")    


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.product_price
        amount+= value
    totalamount = amount + 0
    return render(request, "add_to_cart.html", locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.product_price
            amount += value
        totalamount = amount + 0
        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,

        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.product_price
            amount += value
        totalamount = amount + 0
        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,

        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart_item = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        cart_item.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.product_price
            amount += value
        totalamount = amount + 0
        data={
            'amount': amount,
            'totalamount': totalamount,

        }
        return JsonResponse(data)

class Checkout(View):
    def get(self, request):
        user = request.user
        add= Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.product_price
            famount += value
        totalamount = famount + 0
        return render(request, "checkout.html", locals())

def PoductDetail(request, pk):
    product = ReuseProducts.objects.get(pk=pk)
    return render(request, "product_detail.html", {"product": product})

def display_my_product(request):
    user = request.user
    product = ReuseProducts.objects.filter(user=user)
    return render(request, "my_reuse_products.html", locals())


class MyProducts(View):
    def get(self, request,pk):
        product = ReuseProducts.objects.get(pk=pk)
        form = ReuseProductForm(instance=product)
        return render(request, "update_products.html", locals())
    def post(self, request,pk):
        obj = ReuseProducts.objects.get(pk=pk)
        form = ReuseProductForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Updated")
            return HttpResponseRedirect("/my-products/")
        else:
            messages.warning(request, "Invalid Data")



class DeleteMyProducts(View):
    def get(self, request, pk):
        obj = ReuseProducts.objects.get(pk=pk)
        obj.delete()
        return HttpResponseRedirect("/reuse/")
