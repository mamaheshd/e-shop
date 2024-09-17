from django.shortcuts import render,redirect
from ecommerceapp.models import *
from django.contrib import messages
from math import ceil
from ecommerceapp import keys
from django.views.decorators.csrf import  csrf_exempt


# Create your views here.
def index(request):
    allProds=[]
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        nSlides=n//4+ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nSlides),nSlides])

    params={'allProds':allProds}
    return render(request,"index.html",params)

def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        desc=request.POST.get("desc")
        pnumber=request.POST.get("pnumber")
        myquery=Contact(name=name, email=email, desc=desc, phonenumber=pnumber)
        myquery.save()
        messages.info(request,"We will back to you soon...")
        return render(request,"contact.html")
    
    return render(request,"contact.html")


def about(request):
    return render(request,"about.html")



def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')
    
    currentuser = request.user.username
    items = Orders.objects.filter(email=currentuser)
    
    order_ids = []
    for i in items:
        if "ShopyCart" in i.oid:  
            order_ids.append(i.oid.replace("ShopyCart", ""))  
    if order_ids:
        
        status = OrderUpdate.objects.filter(order_id__in=order_ids)
    else:
        status = [] 
    
    context = {"items": items, "status": status}
    return render(request, "profile.html", context)


