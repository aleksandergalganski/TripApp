from .models import Post, Comment
from .forms import CommentForm, PostForm

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Count

from taggit.models import Tag


def home(request):
    if request.user.is_authenticated:
        return redirect('posts:posts_list')
    return render(request, 'posts/home.html', {})


@login_required
def posts_list(request):
    posts_list = Post.actives.order_by('created')
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


@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(data=request.POST, files=request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            # saving tags
            post_form.save_m2m()
            messages.success(request, 'New post successfully created')
            return redirect(new_post.get_absolute_url())
    else:
        post_form = PostForm()
    return render(request, 'posts/post_create.html', {'post_form': post_form})


@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.user:
        raise PermissionDenied
    else:
        if request.method == 'POST':
            post_form = PostForm(data=request.POST, files=request.FILES,
                                 instance=post)
            if post_form.is_valid():
                post_form.save()
                messages.success(request, 'Your post has been updated')
                return redirect(post.get_absolute_url())
        else:
            post_form = PostForm(instance=post)

        return render(request, 'posts/post_update.html', {'post_form': post_form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.user:
        raise PermissionDenied
    else:
        if request.method == 'POST':
            post.delete()
            messages.success(request, 'Your post has been deleted')
            return redirect('posts:posts_list')
        return render(request, 'posts/post_delete_confirm.html', {'post': post})


@login_required
def tagged_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts_list = Post.objects.filter(tags__in=[tag]).order_by('-created')
    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')
    posts = None

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'posts/posts_list.html', {'posts': posts, 'page': page, 'tag': tag})


@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    return redirect(post.get_absolute_url())


@login_required
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.user:
        raise PermissionDenied
    else:
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST, instance=comment)
            if comment_form.is_valid():
                comment_form.save()
                messages.success(request, 'Your comment has been updated')
                return redirect(reverse('posts:post_detail', args=[comment.post.pk]))
        else:
            comment_form = CommentForm(instance=comment)
        return render(request, 'posts/comment_update.html', {'comment_form': comment_form, 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post = get_object_or_404(Post, pk=comment.post.pk)
    if request.user != comment.user:
        raise PermissionDenied
    else:
        if request.method == 'POST':
            comment.delete()
            messages.success(request, 'Your comment has been deleted')
            return redirect(reverse('posts:post_detail', args=[comment.post.pk]))
        return render(request, 'posts/comment_delete_confirm.html', {'post': post})


@login_required
def popular_tag_list(request):
    tags = Post.tags.most_common()[:10]
    return render(request, 'posts/popular_tag_list.html', {'tags': tags})


@login_required
def popular_location_list(request):
    locations = Post.objects.values('location').annotate(my_count=Count('location')).order_by('-my_count')[:10]
    return render(request, 'posts/popular_location_list.html', {'locations': locations})
