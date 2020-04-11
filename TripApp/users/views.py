from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Profile
from .forms import UserEditForm, ProfileEditForm
from posts.models import Post


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName', False)
        username = request.POST.get('username', False)
        email = request.POST.get('email', False)
        password = request.POST.get('password',False)
        password2 = request.POST.get('password2', False)

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Please use another username')
                return redirect('users:register')
            else:
                user = User.objects.create_user(first_name=first_name, username=username,
                                                password=password, email=email)
                user.save()
                # Create profile for new user
                Profile.objects.create(user=user)
                messages.info(request, 'Your account has been created!')
                return redirect('users:login')
        else:
            messages.info(request, 'Password didnt\'t match')
            return redirect('users:register')
    else:
        return render(request, 'users/registration/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)

        user = authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('posts:posts_list')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('users:login')
    else:
        return render(request, 'users/registration/login.html')


def logout(request):
    auth.logout(request)
    return redirect('logout.html')


@login_required
def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    posts = Post.objects.filter(user=user).order_by('-created')
    posts_count = user.profile.get_posts_count()
    user_likes_count = user.profile.get_total_likes_count()
    return render(request, 'users/user_detail.html', {'user': 'user',
                                                      'posts': 'posts',
                                                      'posts_count': 'posts_count',
                                                      'likes_count': 'likes_count'})


@login_required
def users_list(request):
    current_user = request.user
    users_list = User.objects.all().exclude(id=current_user.id)
    users = None
    paginator = Paginator(users_list, 5)
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'users/users_list.html', {'page': page, 'users': users})


@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.user != user:
        raise PermissionDenied
    else:
        if request.method == 'POST':
            user_form = UserEditForm(data=request.POST, files=request.FILES)
            profile_form = ProfileEditForm(data=request.POST, files=request.FILES)

            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                profile = profile_form.save()
                messages.success(request, 'Your account has been updated')
                return redirect('users:user_detail', username=user.username)
        else:
            user_form = UserEditForm(instance=user)
            profile_form = ProfileEditForm(instance=user.profile)

    return render(request, 'users/edit_profile.html', {'user_form': user_form,
                                                       'profile_form': profile_form})


@login_required
def delete_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.user != user:
        raise PermissionDenied
    else:
        if request.method == 'POST':
            user.delete()
            messages.success(request, 'Your account has been deleted')
            return redirect('posts:home')
    return render(request, 'users/confirm_delete_user.html')
