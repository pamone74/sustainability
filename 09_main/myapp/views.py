from django.shortcuts import render
from .models import Product, ProfileUser, ReuseProducts, Cart, Customer,Ownership, CartOwnerShip
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
from rest_framework import viewsets
from .serializers import ProductSerializer , ProfileUserSerializer, OwnershipSerializer
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import F


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

# Updating profile once the user just created the Account
class Profileview(View):
    def get(self, request):
      form = ProfileForm()
      return render(request, "create_profile.html", locals())
    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            reg_date = date.today()
            reg = ProfileUser(
                user=request.user, 
                full_name=form.cleaned_data["full_name"],
                address=form.cleaned_data["address"],
                city=form.cleaned_data["city"], 
                phone=form.cleaned_data["phone"], 
                date_created=reg_date,
                date_updated=reg_date, 
                country="UAE", 
                country_origin=form.cleaned_data["country_origin"], 
                email=request.user.email,
                reuse_rewards=50,
                recycle_rewards=50,
                recover_rewards=50,
                reduce_rewards=50,
                user_type= form.cleaned_data["user_type"]
                )
            reg.save()
            messages.success(request, "Profile Updated")
            return HttpResponseRedirect("/information/")
        else:
            messages.warning(request, "Invalid Data")
        return render(request, "profile.html", locals())



def Information(request):
    info = ProfileUser.objects.get(user=request.user)
    if info:
        total = info.reuse_rewards + info.recycle_rewards + info.recover_rewards + info.reduce_rewards
    else:
        total = 0
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

# ================= User Dashboard on login ==================================================================================================
# ================= This is the user dashboard that will be displayed once the user logs in===================================================
def dashboard(request):
    profile = ProfileUser.objects.get(user=request.user)
    total_points = profile.reuse_rewards + profile.recycle_rewards + profile.recover_rewards + profile.reduce_rewards
    try:
        total_products = CartOwnerShip.objects.filter(user=request.user).count()
    except ObjectDoesNotExist:
        total_products = 0
    return render(request, 'dashboard_templates/dashboard.html', locals())

def create_product(request):
    return render(request, 'create_product.html',{})

def contact(request):
    return render(request, 'contact.html', {})

# ==================== This is the function that will be used to update the user profile =====================================================
class UpdateInformation(View):
    def get(self, request, pk):
        obj = ProfileUser.objects.get(pk=pk)
        form = ProfileForm(instance=obj)
        return render(request, "update.html", locals())
    def post(self, request, pk):
        obj = ProfileUser.objects.get(pk=pk)
        form = ProfileForm(request.POST, request.FILES,instance=obj)
        print("I am here")
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
    product_id = request.GET.get("pro_id")
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
                    #  We generate the unique Id and decode into  utf-8 format
                    uuid_cal = uuid.uuid1()
                    unid_bytes = uuid_cal.bytes
                    encoded_base = base64.urlsafe_b64encode(unid_bytes).decode('utf-8')
                    # form.instance.product_id = str(encoded_base+"PDF")
                    unique_id = str(encoded_base+"PDF")
                    with open(generate_pdf(qr_code, f"{current_date}.pdf"), "rb") as f:
                        form.instance.product_pdf.save(f"{current_date}{user}.pdf", f, save=True)
                    ownership = Ownership(user=request.user, product=form.instance, status="NO", new_owner=user, product_quantity=form.cleaned_data["product_quantity"], action="Added product", product_uid=unique_id)

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
                cart_update = CartOwnerShip(user=request.user, product=form.instance,mode="Added Product", quantity = form.cleaned_data["product_quantity"], product_uid=unique_id)

                form.save()
                ownership.save()
                cart_update.save()
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
                chosen_product = form.cleaned_data["product_cart"]
                chosen_product_qty = form.cleaned_data["product_quantity"]
                product = Product.objects.filter(product_name=chosen_product).first()
                cart_product = CartOwnerShip.objects.filter(product=product).first()
                product_id = product.product_id
                if chosen_product_qty == 0:
                    messages.warning(request, "Quantity cannot be 0")
                    return render(request,"transfer_product.html", locals())
                if cart_product.quantity < chosen_product_qty and chosen_product_qty > 0:
                    self.denied = True
                    self.no_product = True
                    messages.warning(request, "Quantity Greater than available")
                    return render(request,"transfer_product.html", locals())
                ownership = Ownership(
                    user=request.user,
                    product=product, 
                    status="NO", 
                    new_owner=form.cleaned_data["new_owner"], 
                    product_quantity=chosen_product_qty, 
                    action="Transfered product",
                    product_uid=product_id
                    )
                ownership.save()
                # Getting uer instance and product instance
                user_instance = User.objects.get(username=form.cleaned_data["new_owner"])
                product_instance = Product.objects.filter(pk=product.pk).first()
                cart_update = CartOwnerShip(user=user_instance, product=product_instance,mode=f"Tranfered by {request.user}",quantity = chosen_product_qty, product_uid=product_id)
                # First tranfer then update the database

                cart_update.save()

                # Once the user has transfered the products, we need to delete it from him since the product has been transferedto another user

                obj = CartOwnerShip.objects.filter(user=request.user, product=product_instance).first()
                print(obj)
                obj.delete()
                
                messages.success(request, "Product Transfered")
                return HttpResponseRedirect("/transfer/?transfer_product=True")
            else:
                form = TransferOwnershipForm(user=request.user)
                messages.warning(request, "Invalid Data")
        return render(request, "transfer_product.html", locals())

def create_tranfer(request):
    items = CartOwnerShip.objects.filter(user=request.user)
    return render(request, "create_tranfer_page.html", locals())

def pending(request):
    items = CartOwnerShip.objects.filter(user=request.user)
    # For the total, we need to calculate the total Qunatity not the number of items that are in the cart
    # here i am caluculating the number just
    total = items.count()
    return render(request, "pending_recyles.html", locals())    


# ============ This is Hardware part =============================

#  This views is for serializing the data to be sent to the frontend as JASON data
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProfileUserViewSet(viewsets.ModelViewSet):
    queryset = ProfileUser.objects.all()
    serializer_class = ProfileUserSerializer
    permission_classes = [permissions.IsAuthenticated]
# @csrf_exempt
class OwnershipViewSet(viewsets.ModelViewSet):
    queryset = Ownership.objects.all()
    serializer_class = OwnershipSerializer
    permission_classes = [permissions.IsAuthenticated]
# @exempt_crsf

@csrf_exempt
def SmartBinRecycle(request):
    if request.method == "GET":
        queryset = Ownership.objects.all()
        ownership_serializer = OwnershipSerializer(queryset,many=True, context={"request": request})
        return JsonResponse(ownership_serializer.data,status=200, safe=False)
    if request.method =="POST":
        flag = True
        user = ""
        product_id = ""
        data = request.POST
        for key, value in data.items():
            if key == "user":
                user = value
            elif key == "product_id":
                product_id = value
        if user and product_id:
            #  i have to check the status if it is recyled or not yet
            user = User.objects.get(username=user)
            profile_user = ProfileUser.objects.filter(user=user).first()
            product = Product.objects.filter(product_id=product_id).first()
            cart_profile = CartOwnerShip.objects.filter(user=user, product=product).first()
            if not cart_profile:
                # if it retuebed Null, it means that the product is not associated with the 
                # username, so we need to add the product to the database and update the ownership
                # If cart_profile is None, handle the case appropriately
                # For now, I am just creating a new product and ownership
                id = uuid()
                Product.objects.create(
                    product_id=id,
                    product_name="Recovery",
                    manufacturer_name=user,
                    manufacture_location="AD",
                    product_type="RC",
                    product_quantity=1,
                    product_mf_date=datetime.datetime.now(),
                    product_expiry_date=datetime.datetime.now(),
                    product_ownership=profile_user,
                    product_pdf=None,
                    product_qr_code=None
                )
                ProfileUser.objects.filter(user=user).update(recycle_rewards=F('recover_rewards') + 50)
                return JsonResponse({"Recover": "recovery."}, status=404)
            else:
                Ownership.objects.create(
                user=user,
                product=product,
                status="RC",
                new_owner=profile_user,
                product_quantity=1,
                action="Recycled product",
                product_uid=product_id,
                product_cart=cart_profile
            )
        
                cart_update = CartOwnerShip.objects.get(product=product)
                # We may ned to make sure the quantity is zero then we can remove otherwise just subtract
                # But for now i am using just one item. 
                if cart_update:
                    cart_update.delete()
                    # After recycling, give the person points
                    ProfileUser.objects.filter(user=user).update(recycle_rewards=F('recycle_rewards') + 50)
                return JsonResponse({"status": "success"}, status=201)
    else:
        return JsonResponse({"Error": "failed"}, status=404)
    

from django.http import JsonResponse
# optimized function
def SmartBinRecycleOpt(request):
    if request.method == "POST":
        user = request.POST.get("user")
        product_id = request.POST.get("product_id")

        if user and product_id:
            try:
                user = User.objects.get(username=user)
                profile_user = ProfileUser.objects.filter(user=user).first()
                product = Product.objects.filter(product_id=product_id).first()
                cart_profile = CartOwnerShip.objects.filter(user=user, product=product).first()

                if not cart_profile:
                    # If cart_profile is None, handle the case appropriately
                    # For now, I am just creating a new product and ownership
                    id = uuid()
                    Product.objects.create(
                        product_id=id,
                        product_name="Recovery",
                        manufacturer_name=user,
                        manufacture_location="AD",
                        product_type="RC",
                        product_quantity=1,
                        product_mf_date=datetime.datetime.now(),
                        product_expiry_date=datetime.datetime.now(),
                        product_ownership=profile_user,
                        product_pdf=None,
                        product_qr_code=None
                    )
                    print("Cart profile does not exist for this user and product.")
                    return JsonResponse({"Recover": "Cart profile does not exist for this user and product."}, status=404)

                Ownership.objects.create(
                    user=user,
                    product=product,
                    status="RC",
                    new_owner=profile_user,
                    product_quantity=1,
                    action="Recycled product",
                    product_uid=product_id,
                    product_cart=cart_profile
                )

                # Delete the CartOwnerShip object
                if cart_profile:
                    cart_profile.delete()
                    # After recycling, give the person points
                    ProfileUser.objects.filter(user=user).update(recycle_rewards=F('recycle_rewards') + 50)

                return JsonResponse({"status": "success"}, status=201)
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({"Error": str(e)}, status=500)
        else:
            return JsonResponse({"Error": "Missing user or product_id"}, status=400)
    else:
        return JsonResponse({"Error": "Method not allowed"}, status=405)


@csrf_exempt
def Userviewsets(request):
    from .serializers import UserSerializer
    if request.method == "GET":
        queryset = User.objects.all()
        user = UserSerializer(queryset, many=True, context={"request": request})
        return JsonResponse(user.data, status=200, safe=False)
    if request.method == "POST":
        data = request.POST
        print(data)
        for key, value in data.items():
            print(key,value)
            if key == "user":
                return JsonResponse({"status": "success"}, status=201)
            elif key == "NotFound":
                return JsonResponse({"Error": "failed"}, status=404)
                
    return JsonResponse({"Error": "failed"}, status=404)
    