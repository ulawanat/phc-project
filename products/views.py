from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone
from django.views.generic import ListView
from django.db.models import Q

def home(request):
    products = Product.objects
    return render(request, 'products/home.html', {'products':products})


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product':product})

@login_required(login_url="/accounts/signup")
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total = product.votes_total + 1
        product.save()
        return redirect('/products/' + str(product.id))

@login_required(login_url="/accounts/signup")
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and bool(request.FILES.get('icon', False)) == True and bool(request.FILES.get('image', False)) == True:
            product = Product()
            try:
                product.icon = request.FILES['icon']
                product.image = request.FILES['image']
            except Exception as error:
                return render(request, 'products/create.html', {'error': 'Icon or image is missing'})
            product.title = request.POST['title'] 
            product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.pub_date = timezone.datetime.now()
            product.votes_total = 1
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error': 'All fields are required'})
    else:    
        return render(request, 'products/create.html')

class SearchResultsView(ListView):
    model = Product
    template_name = 'products/search.html'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
        return object_list