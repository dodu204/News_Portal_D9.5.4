from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Category, Article
from .forms import SubscribeForm, UnsubscribeForm


@login_required
def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            categories = form.cleaned_data['categories']
            for category in categories:
                category.subscribers.add(request.user)
            return redirect('home')  # Замените 'home' на URL вашей главной страницы
    else:
        form = SubscribeForm()
    return render(request, 'subscribe.html', {'form': form})


@login_required
def unsubscribe(request):
    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            categories = form.cleaned_data['categories']
            for category in categories:
                category.subscribers.remove(request.user)
            return redirect('home')  # Замените 'home' на URL вашей главной страницы
    else:
        form = UnsubscribeForm()
    return render(request, 'unsubscribe.html', {'form': form})


def home(request):
    categories = Category.objects.all()
    articles = Article.objects.order_by('-created_at')[:5]
    return render(request, 'home.html', {'categories': categories, 'articles': articles})
