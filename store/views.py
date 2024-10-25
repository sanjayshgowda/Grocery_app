from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib import messages


# View for displaying product details
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_details.html', {'product': product})

# Restrict the view to superusers only
@user_passes_test(lambda u: u.is_superuser)
def manage_products(request):
    products = Product.objects.all()
    category = Category.objects.all()
    return render(request, 'store/manage_products.html', {'products': products, 'category': category})

# Add a new product
@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES )
        if form.is_valid():
            print('adding product')
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('manage_products')
    else:
        form = ProductForm()
        
    return render(request, 'store/add_product.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('manage_products')  # Redirect to the same page or another page
    else:
        form = CategoryForm()

    return render(request, 'store/add_category.html', {'form': form})


# Edit an existing product
@user_passes_test(lambda u: u.is_superuser)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/edit_product.html', {'form': form, 'product': product})

# Delete a product
user_passes_test(lambda u: u.is_superuser)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('manage_products')  # Redirect to the product list page after deletion
    
    return render(request, 'store/delete_product.html', {'product': product})

# Product List View
def product_list(request):
    categories = Category.objects.all().order_by('name')
    category_id = request.GET.get('category')  # Get category id from query parameters
    if category_id:
        products = Product.objects.filter(category_id=category_id)  # Filter by selected category
    else:
        products = Product.objects.all()  # Show all products if no category selected

    context = {'categories': categories, 'products': products}
    return render(request, 'store/product_list.html', context)


# Product Detail View
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

# Add Product to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

# Cart Detail View
@login_required
def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in items)
    context = {'items': items, 'total_price': total_price}
    return render(request, 'store/cart.html', context)
'''
@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        items = CartItem.objects.filter(cart=cart)
        cart_items = cart.items.all()  # Fetch all items in the user's cart
    except Cart.DoesNotExist:
        cart_items = []

    return render(request, 'store/cart.html', {'cart_items': cart_items})
'''
@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully.')
        else:
            cart_item.delete()  # If quantity is 0, remove the item from the cart
            messages.success(request, 'Item removed from cart.')

    return redirect('cart_detail')

@login_required
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart_detail'   )

# Order Checkout
@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        items = CartItem.objects.filter(cart=cart)
        total_amount = sum(item.product.price * item.quantity for item in items)

        if items.count() == 0:
            messages.error(request, 'Your cart is empty.')
            return redirect('product_list')
        
        elif request.method == 'POST':
            shipping_address = request.POST.get('shipping_address')
            
            
            # Create order
            order = Order.objects.create(user=request.user, cart=cart, total_amount=total_amount, shipping_address=shipping_address)
            # Clear the cart
            items.all().delete()  # Remove all items from the cart
            
            messages.success(request, 'Order placed successfully!')

            # Redirect to order confirmation page or another page
            return redirect('order_confirmation', order_id=order.id)

    except Cart.DoesNotExist:
        cart_items = []

    return render(request, 'store/checkout.html', {'cart_items': items, 'total_amount': total_amount})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after registration
            messages.success(request, 'Registration successful!')
            return redirect('product_list')
    else:
        form = UserRegisterForm()
    return render(request, 'store/register.html', {'form': form})

# User Login View (optional if using Django's default login view)
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('product_list')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

# User Logout View
def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('product_list')

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/orders.html', {'order': order})

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    categories = Category.objects.all()
    return render(request, 'store/admin_dashboard.html', {'categories': categories})

@user_passes_test(lambda u: u.is_superuser)
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('manage_products')  # Redirect to category list or admin dashboard
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'store/edit_category.html', {'form': form, 'category': category})

@user_passes_test(lambda u: u.is_superuser)
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('manage_products')  # Redirect to the category list page after deletion
    
    return render(request, 'store/delete_category.html', {'category': category})

def home(request):
    return render(request, 'home/home.html')