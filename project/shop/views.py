from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from datetime import datetime

from shop.models import Section, Item, Article, Review, User, Order, OderedItem
from shop.forms import ReviewForm, LoginForm, SignupForm


def main_page_view(request):
    articles = Article.objects.all().order_by('published_at')
    new_page = request.GET.get('page')
    id = request.GET.get('article')

    for article in articles:
        request.session[article.id] = 1

    if new_page and id:
        request.session[int(id)] = new_page
        request.session.modified = True

    return render(
        request,
        'index.html',
        {
            'articles': articles,
        }
    )

def subsection_view(request, section_name, subsection_name=None):
    template = 'empty_section.html'
    section = get_object_or_404(Section, slug=section_name)
    context = {
        'section': section
    }
    
    if subsection_name:
        subsection = get_object_or_404(Section, slug=subsection_name)
        curr_page = request.GET.get('page') or 1
        curr_items = subsection.paginator().get_page(curr_page)
        
        template = 'section.html'
        context['subsection'] = subsection
        context['items'] = curr_items
    
    return render(
        request,
        template,
        context,
    )

def item_view(request, section_name, subsection_name, item_name):
    form = ReviewForm()
    item = get_object_or_404(Item, slug=item_name)
    reviews = Review.objects.filter(item=item)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                item=item,
                name=form.cleaned_data['name'],
                text=form.cleaned_data['text'],
                stars=form.cleaned_data['stars'],
            )
            return redirect(f'/catalog/{section_name}/{subsection_name}/{item_name}')
    
    return render(
        request,
        'item_page.html',
        {
            'item': item,
            'reviews': reviews,
            'form': form,
        }
    )

def login(request):
    form = LoginForm()
    is_error = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            try:
                user = authenticate(username=User.objects.get(email=email).username, password=password)
                if user is not None:
                    auth_login(request, user)

                    return redirect(f'/')
                else:
                    is_error = True
                    
            except User.DoesNotExist:
                is_error = True

                
    return render(
        request,
        'login.html',
        {
            'form': form,
            'is_error': is_error
        }
    )

def signup(request):
    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(email=email, password=password, username=username)
            return redirect('/login/')
    
    return render(
        request,
        'signup.html',
        {
            'form': form
        }
    )

def logout(request):
    auth_logout(request)
    return redirect('/')

def cart_view(request):
    context = {}
    if request.user.is_authenticated:
        context['cart'] = request.user.cart()
    else:
        return redirect('/login/')
    
    return render(
        request,
        'cart.html',
        context
    )

def add_to_cart(request):
    if request.user.is_authenticated:
        item = Item.objects.get(id=request.GET.get('id'))
        user = request.user
        redirect_to = request.GET.get('from') or '/cart'
        for cart_item in user.cart():
            if cart_item.item == item:
                cart_item.quantity += 1
                cart_item.save()
                return redirect(redirect_to)
            
        user.cart().create(user=user, item=item, quantity=1)
        return redirect(redirect_to)
    else:
        return redirect('/login')

def make_order(request):
    user = request.user
    order = Order.objects.create(user=user, order_time=datetime.now())
    for item in user.cart():
        OderedItem.objects.create(item=item.item, order=order, quantity=item.quantity)

    user.cart().delete()
    return render(request, 'thanks_for_order.html')