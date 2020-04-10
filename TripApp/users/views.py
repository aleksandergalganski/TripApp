from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Profile
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm


def register(request):
    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.set_password(register_form.cleaned_data['password'])
            new_user.save()
            # Create new profile associated with new user
            Profile.objects.create(user=new_user)
            messages.success(request, 'Your account has been created')
            return render(request, 'account/register_done.html')
    else:
        register_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'register_form': register_form})
