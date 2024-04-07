from django.shortcuts import render
from .models import Product, ProfileUser, ReuseProducts, Cart, Customer,Ownership
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import NameForm, ProductForm, EventForm, RegistrationForm, ProfileForm, ReuseProductForm, TransferOwnershipForm, SmartDustBinForm   
from django.views import View
from django.contrib import messages
from datetime import date
from django.db.models import Q
from django.contrib.auth.models import User
import uuid
from .QrCode import generate_item_list, generate_pdf, generate_qr_code, extract_images_from_pdf, read_qr_code
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
import os
import shutil
import base64
from django.db import transaction

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
        return HttpResponseRedirect("/account/login/")


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

def dashboard(request):
    return render(request, 'dashboard_templates/dashboard.html', {})

def create_product(request):
    return render(request, 'create_product.html', {})

def contact(request):
    return render(request, 'contact.html', {})


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


#  Themes For 4RS

def reduce(request):
    return render(request, 'reduce.html', {})

def recycle(request):
    return render(request, 'recycle.html', {})

def recover(request):
    return render(request, 'recover.html', {})

class CreateProduct(View):
    submitted = False
    reject= False
    not_profile_user = False
    def get(self, request):
        if "submitted" in request.GET:
            submitted = True
        try:
            user= ProfileUser.objects.get(user=request.user)
        except ObjectDoesNotExist:
            not_profile_user = True
            return render(request, "create_product.html", locals())
        if user.user_type == "MC":
            form = ProductForm()
            return render(request, "create_product.html", locals())
        else:
            reject = True
            return render(request, "create_product.html", locals())
    def post(self, request):
        user = ProfileUser.objects.get(user=request.user)
        if user.user_type == "MC":

            form = ProductForm(request.POST,request.FILES)

            if form.is_valid():
                current_date = datetime.date.today()

                qr_code = generate_item_list(form.cleaned_data["product_name"],form.cleaned_data["product_type"],form.cleaned_data["product_quantity"], request.user, "Not recycled")

                form.instance.product_ownership = user
                # If the qr_code retuned lists of QRCODES, then they are stored in a pdf
                if isinstance(qr_code, list):
                    uuid_cal = uuid.uuid1()
                    unid_bytes = uuid_cal.bytes
                    encoded_base = base64.urlsafe_b64encode(unid_bytes).decode('utf-8')
                    form.instance.product_id = str(encoded_base+"PDF")
                    with open(generate_pdf(qr_code, f"{current_date}.pdf"), "rb") as f:
                        form.instance.product_pdf.save(f"{current_date}{user}.pdf", f, save=True)
                else:
                    unique_id = qr_code.get("random_number", None)
                    form.instance.product_id = unique_id
                    qr_code_filename = qr_code.get('qr_filename', None)
                    if qr_code_filename:
                        form.instance.product_qr_code = qr_code_filename
                        product_pdf = generate_pdf(qr_code, f"{current_date}.pdf")
                        with open(product_pdf, "rb") as f:
                            form.instance.product_pdf.save(f"{current_date}{user}.pdf", f, save=True)
                        shutil.move(qr_code_filename, "media/")
                        os.remove(f"{current_date}.pdf")

                ownership = Ownership(user=request.user, product=form.instance, status="NO", new_owner=user, product_quantity=form.cleaned_data["product_quantity"], action="Added product", product_uid=unique_id)

                form.save()
                ownership.save()
                messages.success(request, "Product Created")
                return HttpResponseRedirect("/create/?submitted=True")
            else:
                messages.warning(request, "Invalid Data")
            return render(request, "create_product.html", locals())
        

# Transfer of products: This is the function that will be used to transfer products from one user to another
class TransferProduct(View):
    no_product = False
    not_allowed = False
    transfer_product = False
    def get(self, request):
        
        if "transfer_product" in request.GET:
            self.transfer_product = True
        
        try:
            form = TransferOwnershipForm(user=request.user)
            if form:
                try:
                    return render(request, "transfer_product.html", locals())
                except ObjectDoesNotExist:
                    self.no_product = True
                    return render(request, "transfer_product.html", locals())
            else:
                self.not_allowed = True
                self.no_product = True
                context ={
                    "not_allowed": self.not_allowed,
                    "no_product": self.no_product,
                }
                return render(request, "transfer_product.html", context)
        except ObjectDoesNotExist:
            self.not_allowed = True
            context ={
                "not_allowed": self.not_allowed
            }
            return render(request, "transfer_product.html", context)
    def post(self, request):
        self.denied = False
        user = ProfileUser.objects.get(user=request.user)
        if user.user_type == "MC":
            form = TransferOwnershipForm(request.POST, request.FILES, user=request.user)
            if form.is_valid():
                chosen_product = form.cleaned_data["product"]
                chosen_product_qty = form.cleaned_data["product_quantity"]
                product = Product.objects.filter(product_name=chosen_product).first()
                product_id = product.product_id
                if chosen_product_qty == 0:
                    messages.warning(request, "Quantity cannot be 0")
                    return render(request,"transfer_product.html", locals())
                if product.product_quantity < chosen_product_qty and chosen_product_qty > 0:
                    self.denied = True
                    self.no_product = True
                    messages.warning(request, "Quantity Greater than available")
                    return render(request,"transfer_product.html", locals())
                form.instance.user = request.user
                form.instance.action = "Transfered product"
                form.instance.product_uid = product_id
                Product.objects.filter(pk=product.pk).update(product_quantity=product.product_quantity - chosen_product_qty)
                form.save()
                messages.success(request, "Product Transfered")
                return HttpResponseRedirect("/transfer/?transfer_product=True")
            else:
                form = TransferOwnershipForm(user=request.user)
                messages.warning(request, "Invalid Data")
            return render(request, "transfer_product.html", locals())
def create_tranfer(request):
    return render(request, "create_tranfer_page.html")



#  Smart BIN
# class SmartBin(View):
#    def get(slef, request):
        #  form = SmartDustBinForm()
        #  return render(request, "smart_dust_bin.html", locals())
#    def post(self, request):
    # form = SmartDustBinForm(request.POST)
    # if form.is_valid():
        # user = form.cleaned_data["name"]
        # location = form.cleaned_data["location"]
        # product_code = form.cleaned_data["product_code"].strip()
        # product_name_f = form.cleaned_data["product_name"]
        # print(product_code)
        # prof_user = ProfileUser.objects.get(user=request.user)
        # Assuming there's a field in Product model called 'pdf_filename' to store the PDF filename
        # with transaction.atomic():
            # try:

                # cart_products = Product.objects.get(product_id = str(product_code))
                # pdt_qty = cart_products.product_quantity
                # print(pdt_qty)
                # if pdt_qty > 0:
                    # cart_products.product_quantity -= 1
                    # cart_products.save()
                # else:
                    # messages.warning(request, "Product quantity is already zero")
                # # # ownership = Ownership(user=cart_products.product_ownership, product=cart_products.product_name, status="RC",   new_owner=cart_products.product_ownership,product_quantity=cart_products.product_quantity, action="Recycled product",product_uid=cart_products.product_id)
                # print("i an here")
                # ownership.save()
                # messages.success(request, "Product recycled succesfully")
                # return HttpResponseRedirect("/create/")
            # except:
                # messages.warning(request, "Product Not found")

        # Check if the items quantity associated with the ID is greater than 1, if so, i means all their qr code are stored in pdf.
        # if cart_products.product_quantity > 1:
            # for product in cart_products:
                # if extract_images_from_pdf( product.product_qr_code.path, str(product_code)):
                    # pd_qty = product.product_quantity
                    # if pd_qty > 0:
                        # product.product_quantity -= 1
                        # product.save()
                    # else:
                        # messages.warning(request, "Product quantity is already zero")
                    # break
                # else:
                    # messages.warning(request, "Product Not found")
        # else:
            # if read_qr_code()
        # return HttpResponseRedirect("/smartbin/")
    # else:
        # messages.warning(request, "Invalid Data")
    # return render(request, "smart_dust_bin.html", locals())