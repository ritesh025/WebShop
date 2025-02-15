from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request):
#  return render(request, 'app/home.html')


class ProductView(View):
    def get(self, request):
        totalitem = 0
        mobiles = Product.objects.filter(category="M")
        laptops = Product.objects.filter(category="L")
        accessories = Product.objects.filter(category="A")
        electronics = Product.objects.filter(category="E")
        watches = Product.objects.filter(category="W")
        cameras = Product.objects.filter(category="C")
        televisions = Product.objects.filter(category="T")
        headphones = Product.objects.filter(category="H")
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(
            request,
            "app/home.html",
            {
                "mobiles": mobiles,
                "laptops": laptops,
                "accessories": accessories,
                "electronics": electronics,
                "watches": watches,
                "cameras": cameras,
                "televisions": televisions,
                "headphones": headphones,
                "totalitem": totalitem,
            },
        )


# def product_detail(request):
#     return render(request, "app/productdetail.html")


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        totalitem = 0
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)
            ).exists()

        return render(
            request,
            "app/productdetail.html",
            {
                "product": product,
                "item_already_in_cart": item_already_in_cart,
                "totalitem": totalitem,
            },
        )


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()

    return redirect("/cart")


@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        Shipping_amount = 100.00
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                tempamount = p.quantity * p.product.discounted_price
                amount += tempamount
                totalamount = amount + Shipping_amount
            return render(
                request,
                "app/addtocart.html",
                {"carts": cart, "totalamount": totalamount, "amount": amount},
            )
        else:
            return render(request, "app/emptycart.html", {"totalitem": totalitem})


def plus_cart(request):
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
    else:
        totalitem = 0

    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(product__id=prod_id, user=request.user)
        c.quantity += 1
        c.save()

        amount = sum(
            p.quantity * p.product.discounted_price
            for p in Cart.objects.filter(user=request.user)
        )
        totalamount = amount + 100  # Including shipping cost

        data = {
            "quantity": c.quantity,
            "amount": amount,
            "totalamount": totalamount,
            "totalitem": totalitem,
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
    else:
        totalitem = 0

    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(product__id=prod_id, user=request.user)

        if c.quantity > 1:
            c.quantity -= 1
            c.save()
        else:
            c.delete()  # If quantity becomes 0, remove item from cart

        amount = sum(
            p.quantity * p.product.discounted_price
            for p in Cart.objects.filter(user=request.user)
        )
        totalamount = amount + 100

        data = {
            "quantity": c.quantity if c.quantity > 0 else 0,
            "amount": amount,
            "totalamount": totalamount,
            "totalitem": totalitem,
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
    else:
        totalitem = 0

    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        Cart.objects.filter(product__id=prod_id, user=request.user).delete()

        amount = sum(
            p.quantity * p.product.discounted_price
            for p in Cart.objects.filter(user=request.user)
        )
        totalamount = amount + 100

        data = {"amount": amount, "totalamount": totalamount, "totalitem": totalitem}
        return JsonResponse(data)


def buy_now(request):
    return render(request, "app/buynow.html")


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, "app/address.html", {"add": add, "active": "btn-primary"})


@login_required
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    op = OrderPlaced.objects.filter(user=request.user)
    return render(
        request, "app/orders.html", {"order_placed": op, "totalitem": totalitem}
    )


def mobile(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        mobiles = Product.objects.filter(category="M")
    elif (
        data == "Samsung"
        or data == "Redmi"
        or data == "Apple"
        or data == "Oppo"
        or data == "Vivo"
        or data == "Realme"
        or data == "Oneplus"
    ):
        mobiles = Product.objects.filter(category="M").filter(brand=data)
    elif data == "below":
        mobiles = Product.objects.filter(category="M").filter(
            discounted_price__lt=20000
        )
    elif data == "above":
        mobiles = Product.objects.filter(category="M").filter(
            discounted_price__gt=20000
        )
    return render(
        request, "app/mobile.html", {"mobiles": mobiles, "totalitem": totalitem}
    )


def laptop(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        laptop = Product.objects.filter(category="L")
    elif (
        data == "Lenovo"
        or data == "ASUS"
        or data == "Acer"
        or data == "MacBook"
        or data == "HP"
        or data == "MSI"
        or data == "Dell"
    ):
        laptop = Product.objects.filter(category="L").filter(brand=data)
    elif data == "below":
        laptop = Product.objects.filter(category="L").filter(discounted_price__lt=30000)
    elif data == "above":
        laptop = Product.objects.filter(category="L").filter(discounted_price__gt=30000)
    return render(
        request, "app/laptop.html", {"laptop": laptop, "totalitem": totalitem}
    )


def camera(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        camera = Product.objects.filter(category="C")
    elif data == "Canon" or data == "Nikon" or data == "Sony":
        camera = Product.objects.filter(category="C").filter(brand=data)
    elif data == "below":
        camera = Product.objects.filter(category="C").filter(discounted_price__lt=60000)
    elif data == "above":
        camera = Product.objects.filter(category="C").filter(discounted_price__gt=60000)
    return render(
        request, "app/camera.html", {"camera": camera, "totalitem": totalitem}
    )


def watches(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        watches = Product.objects.filter(category="W")
    elif (
        data == "Titan"
        or data == "Noise"
        or data == "Fastrack"
        or data == "Boat"
        or data == "Casio"
    ):
        watches = Product.objects.filter(category="W").filter(brand=data)
    elif data == "below":
        watches = Product.objects.filter(category="W").filter(discounted_price__lt=2000)
    elif data == "above":
        watches = Product.objects.filter(category="W").filter(discounted_price__gt=2000)
    return render(
        request, "app/watches.html", {"watches": watches, "totalitem": totalitem}
    )


def headphones(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        headphones = Product.objects.filter(category="H")
    elif (
        data == "JBL"
        or data == "Sony"
        or data == "Samsung"
        or data == "Boat"
        or data == "Zebronics"
        or data == "Oneplus"
        or data == "Realme"
    ):
        headphones = Product.objects.filter(category="H").filter(brand=data)
    elif data == "below":
        headphones = Product.objects.filter(category="H").filter(
            discounted_price__lt=2000
        )
    elif data == "above":
        headphones = Product.objects.filter(category="H").filter(
            discounted_price__gt=2000
        )
    return render(
        request,
        "app/headphones.html",
        {"headphones": headphones, "totalitem": totalitem},
    )


def accessories(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        accessories = Product.objects.filter(category="A")
    elif (
        data == "Boat"
        or data == "Redragon"
        or data == "Logitech"
        or data == "Zebronics"
        or data == "Portronics"
        or data == "HP"
        or data == "MI"
    ):
        accessories = Product.objects.filter(category="A").filter(brand=data)
    elif data == "below":
        accessories = Product.objects.filter(category="A").filter(
            discounted_price__lt=2000
        )
    elif data == "above":
        accessories = Product.objects.filter(category="A").filter(
            discounted_price__gt=2000
        )
    return render(
        request,
        "app/accessories.html",
        {"accessories": accessories, "totalitem": totalitem},
    )


def television(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        television = Product.objects.filter(category="T")
    elif (
        data == "Samsung"
        or data == "MI"
        or data == "LG"
        or data == "Acer"
        or data == "Sony"
    ):
        television = Product.objects.filter(category="T").filter(brand=data)
    elif data == "below":
        television = Product.objects.filter(category="T").filter(
            discounted_price__lt=30000
        )
    elif data == "above":
        television = Product.objects.filter(category="T").filter(
            discounted_price__gt=30000
        )
    return render(
        request,
        "app/television.html",
        {"television": television, "totalitem": totalitem},
    )


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", {"form": form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations!! Registered Successfully.")
            form.save()
        return render(request, "app/customerregistration.html", {"form": form})


@login_required
def checkout(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    Shipping_amount = 100.0
    amount = 0.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        totalamount = amount + Shipping_amount
    return render(
        request,
        "app/checkout.html",
        {
            "add": add,
            "totalamount": totalamount,
            "cart_items": cart_items,
            "totalitem": totalitem,
        },
    )


def payment(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    Shipping_amount = 100.0
    amount = 0.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        totalamount = amount + Shipping_amount
    return render(
        request,
        "app/payment.html",
        {
            "add": add,
            "totalamount": totalamount,
            "cart_items": cart_items,
            "totalitem": totalitem,
        },
    )


@login_required
def payment_done(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    cart = Cart.objects.filter(user=user)
    print(cart)
    for c in cart:
        OrderPlaced(
            user=user, customer=customer, product=c.product, quantity=c.quantity
        ).save()
        c.delete()
    return redirect("orders")


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(
            request, "app/profile.html", {"form": form, "active": "btn-primary"}
        )

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data["name"]
            locality = form.cleaned_data["locality"]
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"]
            zipcode = form.cleaned_data["zipcode"]
            reg = Customer(
                user=usr,
                name=name,
                locality=locality,
                city=city,
                state=state,
                zipcode=zipcode,
            )
            reg.save()

            messages.success(request, "Congratulations!! Profile Updated Successfully.")
        return render(
            request, "app/profile.html", {"form": form, "active": "btn-primary"}
        )
