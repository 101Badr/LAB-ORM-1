from django.shortcuts import render, redirect, get_object_or_404
from .models import Post


def home(request):
    posts = Post.objects.filter(
        is_published=True
    ).order_by('-published_at')

    return render(request, 'posts/home.html', {
        'posts': posts
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    return render(request, 'posts/detail.html', {
        'post': post
    })


def add_post(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        if title and content and len(title) <= 2048:
            Post.objects.create(
                title=title,
                content=content,
                poster=request.FILES.get('poster', 'images/default.jpg')
            )
            return redirect('posts:home')

        return render(request, 'posts/add_post.html', {
            'error': 'Please enter a valid title and content.'
        })

    return render(request, 'posts/add_post.html')

def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        if title and content and len(title) <= 2048:
            post.title = title
            post.content = content

            if request.FILES.get('poster'):
                post.poster = request.FILES['poster']

            post.save()

            return redirect('posts:detail', post_id=post.id)

        return render(request, 'posts/update_post.html', {
            'post': post,
            'error': 'Please enter a valid title and content.'
        })

    return render(request, 'posts/update_post.html', {
        'post': post
    })

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        post.delete()
        return redirect('posts:home')

    return render(request, 'posts/delete_post.html', {
        'post': post
    })