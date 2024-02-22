from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404, render
from . models import CATEGORY,PRODUCTS ,Cart,Cartitem
from django.core.paginator import Paginator, EmptyPage,InvalidPage
from django.db.models import  Q
from django.core.exceptions import  ObjectDoesNotExist
from django.urls import reverse

# Create your views here.

# def allprodcat(request,c_slug=None):
#     c_page=None
#     products_list=None
#     if c_slug!=None:
#         c_page=get_object_or_404(CATEGORY,slug=c_slug)
#         products_list=PRODUCTS.objects.all().filter(category=c_page,available=True)
#     else:
#         products_list=PRODUCTS.objects.all().filter(available=True)
#     paginator=Paginator(products_list,6)
#     try:
#         page=int(request.GET.get('page','1'))
#     except:
#         page=1
#     try:
#         products=paginator.page(page)
#     except (EmptyPage,InvalidPage):
#         products=paginator.page(paginator.num_pages)        
#     return  render(request,"category.html",{'category':c_page,'products':products}) 



def allprodcat(request, c_slug=None):
    c_page = None
    products_list = None

    # Filter products by category if category slug is provided
    if c_slug:
        c_page = get_object_or_404(CATEGORY, slug=c_slug)
        products_list = PRODUCTS.objects.filter(category=c_page, available=True)
    else:
        products_list = PRODUCTS.objects.filter(available=True)

    # Paginate the products list
    paginator = Paginator(products_list, 6)
    page_number = request.GET.get('page')

    try:
        products = paginator.page(page_number)
    except InvalidPage:
        # If page is not an integer, deliver first page
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        products = paginator.page(paginator.num_pages)

    return render(request, "category.html", {'category': c_page, 'products': products})

def proDetail(request,c_slug,product_slug):
    try:
        products=PRODUCTS.objects.get(category__slug=c_slug,slug=product_slug)
    except Exception as e:
        raise e 
    return render(request,'product.html',{'products':products})   

# def SearchResuls(request):
#     products=None
#     query=None
#     if 'q' in request.GET:
#         query = request.GET('q')
#         products = PRODUCTS.objects.all().filter(Q(name__contains=query)) | Q(description__contains=query)
#         return render(request,'search.html',{'query':query, 'products':products} )

def SearchResuls(request):
    query = request.GET.get('q')

    if query:
        # Perform search query using your model's fields
        results = PRODUCTS.objects.filter(name__icontains=query)  # Example: searching by product name
    else:
        results = []

    return render(request, 'search.html', {'results': results, 'query': query})
# from django.shortcuts import render, redirect
# from django.core.exceptions import ObjectDoesNotExist
# from .models import PRODUCTS, Cart, Cartitem

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
        cart = request.session.session_key
    return cart

def add_cart(request, product_id):
    product = PRODUCTS.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    
    try:
        cart_item = Cartitem.objects.get(cart=cart, product=product)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except Cartitem.DoesNotExist:
        cart_item = Cartitem.objects.create(cart=cart, product=product, quantity=1)
    
    # Redirect to the cart detail page
    return redirect("shop:cart_detail")

def cart_detail(request):
    total = 0
    counter = 0
    cart_items = None
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = Cartitem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total, 'counter': counter})
   
def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(PRODUCTS, id=product_id)
    cart_item = Cartitem.objects.filter(product=product, cart=cart).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('shop:cart_detail')
def full_remove(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(PRODUCTS,id=product_id)
    cart_item=Cartitem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('shop:cart_detail')
