from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Cart, CartItem, Order, OrderItem


# ─── HELPERS ────────────────────────────────────────────────────────────────

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, session_key=None)
        # Merge session cart if exists
        session_key = request.session.session_key
        if session_key:
            try:
                session_cart = Cart.objects.get(session_key=session_key, user=None)
                for item in session_cart.items.all():
                    existing = cart.items.filter(product=item.product).first()
                    if existing:
                        existing.quantity += item.quantity
                        existing.save()
                    else:
                        item.cart = cart
                        item.save()
                session_cart.delete()
            except Cart.DoesNotExist:
                pass
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
    return cart


# ─── HOME ────────────────────────────────────────────────────────────────────

def home(request):
    categories = Category.objects.all()
    featured = Product.objects.filter(is_featured=True)[:8]
    all_products = Product.objects.all().order_by('-created_at')

    category_slug = request.GET.get('category')
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort', '')

    if category_slug:
        all_products = all_products.filter(category__slug=category_slug)
    if query:
        all_products = all_products.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)
        )
    if min_price:
        all_products = all_products.filter(price__gte=min_price)
    if max_price:
        all_products = all_products.filter(price__lte=max_price)
    if sort == 'price_low':
        all_products = all_products.order_by('price')
    elif sort == 'price_high':
        all_products = all_products.order_by('-price')
    elif sort == 'rating':
        all_products = all_products.order_by('-rating')
    elif sort == 'newest':
        all_products = all_products.order_by('-created_at')

    active_category = None
    if category_slug:
        try:
            active_category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            pass

    context = {
        'categories': categories,
        'featured_products': featured,
        'products': all_products,
        'query': query,
        'active_category': active_category,
        'sort': sort,
        'min_price': min_price or '',
        'max_price': max_price or '',
    }
    return render(request, 'store/home.html', context)


# ─── PRODUCT DETAIL ──────────────────────────────────────────────────────────

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    context = {'product': product, 'related_products': related}
    return render(request, 'store/product_detail.html', context)


# ─── SEARCH ──────────────────────────────────────────────────────────────────

def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)
    ) if query else Product.objects.none()
    return render(request, 'store/search_results.html', {'products': products, 'query': query})


# ─── CART ────────────────────────────────────────────────────────────────────

def cart_view(request):
    cart = get_or_create_cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'"{product.name}" added to cart!')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    qty = int(request.POST.get('quantity', 1))
    if qty < 1:
        item.delete()
    else:
        item.quantity = qty
        item.save()
    return redirect('cart')


# ─── CHECKOUT ────────────────────────────────────────────────────────────────

@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
            payment_method=request.POST.get('payment_method', 'cod'),
            total_price=cart.total_price,
            payment_status=True,
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            # Reduce stock
            item.product.stock -= item.quantity
            item.product.save()
        cart.items.all().delete()
        return redirect('order_success', order_id=order.id)

    context = {
        'cart': cart,
        'user': request.user,
    }
    return render(request, 'store/checkout.html', context)


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_success.html', {'order': order})


# ─── ORDER HISTORY ───────────────────────────────────────────────────────────

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


# ─── AUTH ────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(request.GET.get('next', '/'))
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'store/login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(
                username=username, email=email,
                password=password, first_name=first_name, last_name=last_name
            )
            login(request, user)
            messages.success(request, f'Account created! Welcome, {first_name}!')
            return redirect('home')
    return render(request, 'store/signup.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'store/profile.html', {'orders': orders})
