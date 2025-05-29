"""from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm

from .models import Product, CartItem, Order, OrderItem
from .forms import CustomUserCreationForm, DeliveryForm, DeliveryAddressForm


def home(request):
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def add_to_cart(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        quantity = int(request.POST.get('quantity', 1))

        # Check if product is in stock
        if product.stock < quantity:
            messages.error(request, f"Only {product.stock} item(s) available in stock.")
            return redirect('product_detail', pk=pk)

        # Get or create the cart item
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity, 'price': product.price}
        )

        if not created:
            new_quantity = cart_item.quantity + quantity

            # Prevent exceeding stock
            if new_quantity > product.stock:
                messages.error(request, f"You already have {cart_item.quantity} item(s) in cart. Only {product.stock - cart_item.quantity} more can be added.")
                return redirect('product_detail', pk=pk)

            cart_item.quantity = new_quantity
            cart_item.save()

        messages.success(request, f"Added {quantity} item(s) of {product.name} to cart.")
        return redirect('cart_detail')
    else:
        return redirect('login')
    

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    form = DeliveryAddressForm(request.POST or None)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update':
            for item in cart_items:
                quantity = request.POST.get(f'quantities_{item.id}')
                if quantity and quantity.isdigit():
                    item.quantity = int(quantity)
                    item.save()
            messages.success(request, "Cart updated!")
            return redirect('cart_detail')

        elif action == 'buy':
            if form.is_valid():
                address = form.cleaned_data.get('address')
                phone = form.cleaned_data.get('phone')

                # Here you should create orders; this example uses a simple Order model
                order = Order.objects.create(user=request.user, address=address)
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price,
                    )
                cart_items.delete()
                messages.success(request, "Your order has been placed successfully!")
                return redirect('home')
            else:
                messages.error(request, "Please enter a valid address.")

    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'catalog/cart_detail.html', {
        'cart_items': cart_items,
        'form': form,
        'total': total,
    })


# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'catalog/signup.html', {'form': form})




def home(request):
    return render(request, 'catalog/home.html')

def search_view(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Product.objects.filter(name__icontains=query)

    return render(request, 'catalog/home.html', {
        'products': results,
        'query': query
    })

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after successful registration
            return redirect('home')  # Redirect to home page or any other page
    else:
        form = CustomUserCreationForm()
    
    # Render the registration template with the form
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def buy_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('cart_detail')

    order = Order.objects.create(user=request.user)
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart_items.delete()
    return redirect('order_success')


def order_success(request):
    return render(request, 'catalog/order_success.html')


@login_required
def update_cart(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('quantities_'):
                cart_item_id = key.split('_')[1]
                try:
                    quantity = int(value)
                    if quantity < 1:
                        quantity = 1
                    cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
                    cart_item.quantity = quantity
                    cart_item.save()
                except (ValueError, CartItem.DoesNotExist):
                    pass
    return redirect('cart_detail')


@login_required
def remove_from_cart(request, cart_item_id):
    item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart_detail')


def cart_checkout(request):
    # Your logic here
    return render(request, 'cart_checkout.html')
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Product, CartItem, Order, OrderItem
from .forms import CustomUserCreationForm, DeliveryForm, DeliveryAddressForm


def home(request):
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def add_to_cart(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        quantity = int(request.POST.get('quantity', 1))

        if product.stock < quantity:
            messages.error(request, f"Only {product.stock} item(s) available in stock.")
            return redirect('product_detail', pk=pk)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity, 'price': product.price}
        )

        if not created:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                messages.error(request, f"You already have {cart_item.quantity} item(s) in cart. Only {product.stock - cart_item.quantity} more can be added.")
                return redirect('product_detail', pk=pk)

            cart_item.quantity = new_quantity
            cart_item.save()

        messages.success(request, f"Added {quantity} item(s) of {product.name} to cart.")
        return redirect('cart_detail')
    else:
        return redirect('login')


@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    form = DeliveryAddressForm(request.POST or None)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update':
            for item in cart_items:
                quantity = request.POST.get(f'quantities_{item.id}')
                if quantity and quantity.isdigit():
                    item.quantity = int(quantity)
                    item.save()
            messages.success(request, "Cart updated!")
            return redirect('cart_detail')

        elif action == 'buy':
            if form.is_valid():
                address = form.cleaned_data.get('address')
                phone = form.cleaned_data.get('phone')

                order = Order.objects.create(user=request.user, address=address)
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price,
                    )
                cart_items.delete()
                messages.success(request, "Your order has been placed successfully!")
                return redirect('home')
            else:
                messages.error(request, "Please enter a valid address.")

    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'catalog/cart_detail.html', {
        'cart_items': cart_items,
        'form': form,
        'total': total,
    })

def search_view(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Product.objects.filter(name__icontains=query)

    return render(request, 'catalog/home.html', {
        'products': results,
        'query': query
    })


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def buy_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('cart_detail')

    order = Order.objects.create(user=request.user)
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart_items.delete()
    return redirect('order_success')


def order_success(request):
    return render(request, 'catalog/order_success.html')


@login_required
def update_cart(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('quantities_'):
                cart_item_id = key.split('_')[1]
                try:
                    quantity = int(value)
                    if quantity < 1:
                        quantity = 1
                    cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
                    cart_item.quantity = quantity
                    cart_item.save()
                except (ValueError, CartItem.DoesNotExist):
                    pass
    return redirect('cart_detail')


@login_required
def remove_from_cart(request, cart_item_id):
    item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart_detail')


def cart_checkout(request):
    return render(request, 'catalog/cart_checkout.html')



def signup(request):
    return render(request, 'signup.html')
