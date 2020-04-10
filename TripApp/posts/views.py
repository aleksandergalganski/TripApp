from .models import Post

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return render(request, 'posts/home.html', {})


@login_required
def posts_list(request):
    posts_list = Post.actives.order_by('-created')
    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')
    posts = None
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'posts/posts_list.html', {'page': page, 'posts': posts})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post__id=post_id)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # Assign the current post to comment
            new_comment.post = post
            # Assign the current user to comment
            new_comment.user = request.user
            new_comment.save()
            messages.success(request, f'Your comment has been added!')
    else:
        comment_form = CommentForm()
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form,
                                                      'new_comment': new_comment})






