from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404,redirect
from .models import Category, Product, Review
from .forms import ProductoForm, ReviewForm
from django.contrib.auth.decorators import user_passes_test, login_required
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from django.db.models import Count

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# Vista para que los usuarios vean la lista de productos // Busqueda por nombre
@login_required
def lista_productos(request):
    query = request.GET.get('q')
    if query:
        productos = Product.objects.filter(name__icontains=query)
    else:
        productos = Product.objects.all()
    return render(request, 'users/product_list.html', {'productos': productos})

# Vista para que los usuarios vean los detalles de un producto
@login_required
def detalle_producto(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})

@login_required #Productos mas vendidos
def top_productos_vendidos(request):
    productos = Product.objects.order_by('-ventas')[:3]
    return render(request, 'users/top_productos.html', {'productos': productos})

@login_required
def productos_mas_comentados(request): #productos con mas reviews
    productos = Product.objects.annotate(num_reviews=Count('reviews')).order_by('-num_reviews')[:4]
    return render(request, 'users/top_comentados.html', {'productos': productos})


@login_required
def agregar_review(request, product_id):
    producto = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = producto  # Asociar la review al producto
            review.user = request.user  # Asociar la review al usuario
            review.save()
            return redirect('detalle_producto', pk=producto.pk)
    else:
        form = ReviewForm()
    
    return render(request, 'productos/agregar_review.html', {'form': form, 'producto': producto})





# Verificación para asegurarse de que el usuario es administrador
def es_admin(user):
    return user.is_superuser or user.role == 'admin'

@user_passes_test(es_admin)
def gestion_productos(request):
    productos = Product.objects.all()
    return render(request, 'admin/gestion_productos.html', {'productos': productos})

@user_passes_test(es_admin)
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gestion_productos')
    else:
        form = ProductoForm()
    return render(request, 'admin/crear_producto.html', {'form': form})

@user_passes_test(es_admin)
def editar_producto(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('gestion_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'admin/editar_producto.html', {'form': form})

@user_passes_test(es_admin)
def eliminar_producto(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('gestion_productos')
    return render(request, 'admin/eliminar_producto.html', {'producto': producto})
