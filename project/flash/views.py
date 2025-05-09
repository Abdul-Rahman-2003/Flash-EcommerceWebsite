from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from . models import * 
from .forms import CustomUserForm
import json
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def home(request):
    categories = Category.objects.filter(status=True).exclude(name="")
    products = Product.objects.filter(status=True)[:8]
    return render(request, "firstpage.html", {"products": products, "categories": categories})


def category_products_men(request):
    men_products = Product.objects.filter(category__name__iexact='Men', status=True).order_by('-id')
    paginator = Paginator(men_products, 22)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "category_name": "Men"
    }
    return render(request, "men.html", context)

    

def category_products_women(request):
    women_products = Product.objects.filter(category__name__iexact='Women', status=True).order_by('-id')
    paginator = Paginator(women_products, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "category_name": "Women"
    }
    return render(request, "women.html", context)


def category_products_kid(request):
    kid_products = Product.objects.filter(category__name__iexact='Kid', status=True).order_by('-id')
    paginator = Paginator(kid_products, 22)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "category_name": "Kid"
    }
    return render(request, "Kid.html", context)

def product_details(request, cname, slug):
    category = Category.objects.filter(slug=cname, status=True).first()
    print("Category Found:", category)

    if category:
        product = Product.objects.filter(category=category, slug=slug, status=True).first()
        print("Product Found:", product)

        if product:
            return render(request, "shop/products/product_details.html", {"product": product})
        else:
            messages.error(request, "No Such Product Found")
            return redirect('collections')
    else:
        messages.error(request, "No Such Category Found")
        return redirect('collections')

    

def search_view(request):
    query=request.GET.get('query')
    results=[]
    if query:
        results=Product.objects.filter(name__icontains=query)
    return render(request,'search_results.html',{"results":results,"query":query})


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_qty = int(request.POST.get('product_qty', 1))

        product = get_object_or_404(Product, id=product_id)

        if product_qty > product.quantity:
            messages.error(request, "Not enough stock available")
            return redirect('Search_results.html')  # Or wherever the search view is

        # Check if product already in cart
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'product_qty': product_qty}
        )
        if not created:
            cart_item.product_qty += product_qty
            cart_item.save()

        messages.success(request, f"Added {product.name} to cart")
        return redirect('search_results.html')  



def favviewpage(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,"fav.html",{"fav":fav})
    else:  
        return redirect("/")
    

def fav_page(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=(data['pid'])
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Favourite'},status=200)
                else:
                    Favourite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status':'Product Added to Favourite'},status=200)
        else:
                return JsonResponse({'status':'Login to Add Favourite'}, status=200)
    else:
            return JsonResponse({'status':'Login to Add Favourite'}, status=200)

    

def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")

def remove_fav(request,fid):
    item=Favourite.objects.get(id=fid)
    item.delete()
    return redirect("/favviewpage")

def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"cart.html",{"cart":cart})
    else:  
        return redirect("/")

def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=(data['pid'])
            #  print(request.user.id)
            product_status = Product.objects.filter(id=product_id).first()
            if product_status:
    # safe to continue
                if Cart.objects.filter(user=request.user,product_id=product_id).exists():
                    return JsonResponse({'status':'Product Already in Cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to the Cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product Stock Not Available'}, status=200)


                
            return JsonResponse({'status':'Product Add TO Cart Success'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)

   
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged Out Successfully")
    return redirect("/")


def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged In Successfully")
                return redirect("/")
            else:
                messages.error(request,"Invalid User Name or Password")
                return redirect("/login")
        return render(request,"login.html")

def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success You Can Login Now..!")
            return redirect('/login')
    return render(request,"registerpage.html",{"form":form})
    
from django.shortcuts import get_object_or_404

def collections(request):
    categories = Category.objects.filter(status=True).exclude(name="")
    return render(request, "collections.html", {"categories": categories})


def collectionsview(request, cname):
    category = Category.objects.filter(slug=cname, status=True).first()
    if category:
        products = Product.objects.filter(category=category)
        return render(request, "shop/products/index.html", {
            "products": products,
            "category_name": category.name
        })
    else:
        messages.warning(request, "NO SUCH CATEGORY FOUND")
        return redirect('collections')
    
def bestseller(request):
    products = Product.objects.filter(trending=1).exclude(name="")
    return render(request,"bestseller.html" , {"products": products})

def upcoming(request):
    return render(request,"upcoming.html")

def arrival(request):
    return render(request,"arrival.html")

    





