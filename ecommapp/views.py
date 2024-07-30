from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from ecommapp.models import Product, Cart, Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail

# Create your views here.
def home(request):
    # return HttpResponse("<i>this is home page</i>")
    context = {}
    context['name'] = "John"
    context["age"] = 10
    context["x"] = 20
    context["y"] = 30
    context["list"] = [1,2,3,4]
    if context["x"] > context["y"]:
        res="x is greater"
    else:
        res="y is greater"

    context["products"] = [
        {'id':1,'name':'kiran','cat':'shoes','price':1000},
        {'id':2,'name':'sarika','cat':'clothe','price':800},
        {'id':3,'name':'ram','cat':'watch','price':3000},
        {'id':4,'name':'sham','cat':'bag','price':500},
        {'id':5,'name':'sanika','cat':'earrings','price':200}
    ]
    return render(request,'home.html',context)

def about(request):
    return HttpResponse("<b>this is about page</b>")

def contact(request, a, b):
    print(a)
    print(type(a))
    if int(a) > int(b):
        result = f"{a} is greater"
    else:
        result = f"{b} is greater"
    return HttpResponse("<h1>this is contact page</h1> "+ result)

class SampleView(View):
    def get(self,request):
        return HttpResponse("Hello from sample view")
    
def index(request):
    p = Product.objects.filter(is_active = True)
    context = {}
    context['products'] = p

    return render(request,'index.html',context)

def about(request):
    return render(request,'about.html')

def cart(request):
    # request.session['user'] = request.user.id
    userid = request.user.id
    c = Cart.objects.filter(uid = userid)
    s = 0
    n = len(c)
    total_qty = 0
    for x in c:
        s = s + x.pid.price * x.qty
        total_qty = total_qty + x.qty
    context = {}
    context['products'] = c
    context['total'] = s
    context['np'] = n
    context['total_qty'] = total_qty
    return render(request,'cart.html',context)

def contact(request):
    return render(request,'contact.html')

def user_login(request):
    context = {}
    if request.method == 'POST':
        uname = request.POST['uname']
        password = request.POST['pass']
        
        if uname == "" or password == "":
            context['errmsg'] = "Fields cannot be empty"
            return render(request,'login.html',context)
        else:
            a = authenticate(username=uname,password=password)
            if a is not None:
                login(request,a)
                return redirect('/index')
            else:
                context['errmsg'] = "Invalid username"
                return render(request, "login.html")
    else:
        return render(request,'login.html')
    
def user_logout(request):
    logout(request)
    return redirect('/login')

def place_order(request):
    userid = request.user.id
    c = Cart.objects.filter(uid = userid)
    oid = random.randrange(1000,9999)

    for x in c:
        o = Order.objects.create(order_id = oid, pid=x.pid, uid = x.uid, qty = x.qty)
        o.save()
        x.delete()
    
    orders = Order.objects.filter(uid= request.user.id)
    s = 0
    n = len(c)
    total_qty = 0
    for x in orders:
        s = s + x.pid.price * x.qty
        total_qty = total_qty + x.qty
    context = {}
    context['products'] = orders
    context['total'] = s
    context['np'] = n
    context['total_qty'] = total_qty
    return render(request,'place_order.html',context)

def product_detail(request, pid):
    p = Product.objects.filter(id=pid)
    context = {}
    context['products'] = p
    return render(request,'product_detail.html',context)

def reg(request):
    context = {}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        pwd = request.POST['pass']
        print(email, password, pwd)
        if email == "" or password == "" or pwd == "":
            return render(request,'register.html')
        else:
            try:
                u = User.objects.create(username=email,email=email)
                u.set_password(password)
                u.save()
                context['success'] = "User created successfully."
                return render(request,'register.html',context)
            except Exception:
                context['errmsg'] = "user with same username"
                return render(request,'register.html',context)      
    return render(request,'register.html')

def catfilter(request, cv):
    q1 = Q(is_active=True)
    q2 = Q(cat=cv)
    p = Product.objects.filter(q1 & q2)
    print(p)
    context = {}
    context['products'] = p
    return render(request,'index.html',context)

def sort(request, sv):
    if sv == '0':
        col='price'
    else:
        col='-price'
    p=Product.objects.filter(is_active=True).order_by(col)
    context = {}
    context['products'] = p
    print(col,p)
    return render(request,'index.html',context)

def range(request):
    min = request.GET['min']
    max = request.GET['max']
    q1 = Q(price__gte = min)
    q2 = Q(price__lte = max)
    q3 = Q(is_active = True)

    p=Product.objects.filter(q1 & q2 & q3)
    context = {}
    context['products'] = p
    return render(request,'index.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        u = User.objects.filter(id = request.user.id)
        p = Product.objects.filter(id = pid)

        context ={}
        context['products'] = p
        q1 = Q(uid=u[0])
        q2 = Q(pid=p[0])
        c = Cart.objects.filter(q1&q2)
        n = len(c)
        if n == 1:
            context['msg'] = "Product already exists in the cart"
            return render(request, "product_detail.html", context)
        else:
            c = Cart.objects.create(uid = u[0], pid = p[0])
            c.save()            
            context['success'] = "Product added successfully to the cart."
            return render(request, "product_detail.html", context)
    else:
        return redirect("/login")
    
def remove(request, cid):
    c = Cart.objects.filter(id = cid)
    c.delete()
    return redirect('/cart')

def updateqty(request, qv, cid):
    c = Cart.objects.filter(id = cid)
    if qv == '1':
        t = c[0].qty + 1
        c.update(qty =t)
    else:
        if c[0].qty > 1:
            t = c[0].qty - 1
            c.update(qty = t)

    return redirect('/cart')    

def makepayment(request):
    orders = Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s + x.pid.price * x.qty
        oid = x.order_id
    client = razorpay.Client(auth=("rzp_test_qPpA776V9DCblP", "TWcWQeLgGmHfG66yYcv7tzhJ"))

    data = { "amount": s * 100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    context = {}
    context['data'] = payment
    return render(request,'pay.html',context)

def sendemail(request):
    useremail = request.user.email
    order_details = ""
    send_mail(
    "Ecart order placed successfully.",
    order_details,
    "rushalibjadhav30895@gmail.com",
    [useremail],
    fail_silently=False,
    )
    return HttpResponse("Mail sent successfully.")