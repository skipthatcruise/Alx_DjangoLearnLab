from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .forms import UserUpdateForm, ProfileUpdateForm

def home(request):
    return render(request, 'blog/home.html')

def posts(request):
    # This is where you would query your database to get posts and pass them to the template
    return render(request, 'blog/posts.html')


#Register View
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')

    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


#Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')

    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

#Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

#Profile view
@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'registration/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

