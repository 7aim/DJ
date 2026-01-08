from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q 
from .models import Category, Post, Author, Book, Tag, Comment

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def homepage (request):
    categories = Category.objects.all()[0:3]
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    context= {
        'object_list': featured,
        'latest': latest,
        'categories':categories,
    }
    return render(request, 'homepage.html',context)

def post (request,slug):
    post = Post.objects.get(slug = slug)
    latest = Post.objects.order_by('-timestamp')[:3]
    
    if request.method == "POST":
        name = request.POST.get("name")
        text = request.POST.get("text")
        if name and text:
            Comment.objects.create(post=post, name=name, text=text)
            return redirect('post', slug=post.slug)
    
    context = {
        'post': post,
        'latest': latest,
    }
    return render(request, 'post.html', context)

def about (request):
    return render(request, 'about_page.html')

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'object_list': queryset
    }
    return render(request, 'search_bar.html', context)


def postlist (request,slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(categories__in=[category])

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)

def allposts(request):
    posts = Post.objects.order_by('-timestamp')

    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)

def books_list(request):
    books = Book.objects.order_by("-created_at")
    return render(request, "books_list.html", {"books": books})

def tags_list(request):  # (3.10)
    tags = Tag.objects.all().order_by("-created_at")
    return render(request, "tags_list.html", {"tags": tags})


def tag_search(request):  # (3.6)
    q = request.GET.get("q", "")
    posts = Post.objects.filter(tags__name__icontains=q).distinct() if q else []
    return render(request, "tag_search.html", {"posts": posts, "q": q})