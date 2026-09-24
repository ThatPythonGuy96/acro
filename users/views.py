from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.contrib import messages
from .forms import CreateUserForm, ProfileChangeForm
from .models import User

class ProfileView(generic.DetailView):
    model = User
    template_name = 'user/profile.html'
    context_object_name = 'user'

def registerview(request):
    if request.user.is_authenticated:
        return redirect('music:index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                myuser = form.cleaned_data.get('username')
                messages.success(request, 'User Account has been Created for ' + myuser)
                return redirect('users:login')
        context = {'form': form,}
        return render(request, 'user/register.html', context)

def loginview(request):
    if request.user.is_authenticated:
        return redirect('music:index')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('music:index')
            else:
                messages.info(request, 'email or Password incorrect')

        context = {}
        return render(request, 'user/login.html', context)

def logoutview(request):
    logout(request)
    return redirect('users:login')

def profileedit(request, pk):
    user = request.user
    form = ProfileChangeForm(instance=user)
    if request.method == 'POST':
        form = ProfileChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    context = {'form': form}
    return render(request, 'user/edit.html', context)

class UserDelete(generic.DeleteView):
    model = User
    pk_url_kwarg = 'pk'
    template_name = 'music/delete.html'
    success_url = reverse_lazy('music:index')
