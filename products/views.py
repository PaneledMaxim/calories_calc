from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Product
from .forms import ProductForm


def product_list_view(request):
    products = Product.objects.all()
    for product in products:
        product.can_edit = product.creator == request.user or request.user.is_staff
        product.can_delete = product.creator == request.user or request.user.is_staff
    return render(request, 'products/product_list.html', {'products': products})


@login_required
def add_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.creator = request.user
            product.save()
            return redirect('products:list')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})


@login_required
def edit_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if product.creator != request.user and not request.user.is_staff:
        raise PermissionDenied("У вас нет прав на редактирование этого продукта")
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/edit_product.html', {'form': form, 'product': product})


@login_required
def delete_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if product.creator != request.user and not request.user.is_staff:
        raise PermissionDenied("У вас нет прав на удаление этого продукта")
    
    if request.method == 'POST':
        product.delete()
        return redirect('products:list')

    return render(request, 'products/delete_product.html', {'product': product})