from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
import json
from django.http import JsonResponse
from owner.models import Category

# Create your views here.

def owner_login(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        return redirect(owner_dashboard)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user:
            auth.login(request,user)
            return JsonResponse('success', safe=False)
        else:
            return JsonResponse('loginfailed', safe=False)
    else:
        return render(request, './owner/Login.html')

def owner_logout(request):
    auth.logout(request)
    return redirect(owner_login)

def owner_dashboard(request):
    return render(request, './owner/Dashboard.html')


def manage_category(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request, './owner/ManageCategory.html',context)

def create_category(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == 'POST':
            category_name = request.POST['category']
            Category.objects.create(category_name=category_name)
            return JsonResponse('category_created', safe=False)
        else:
            return render(request, './owner/CreateCategory.html')
    else:
        return redirect(owner_login)


def edit_category(request,id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        category = Category.objects.get(id=id)
        if request.method == 'POST':
            category_name = request.POST['category_name']
            category.category_name = category_name
            category.save()
        else:
            context = {'category':category}
            return render(request, './owner/EditCategory.html',context)
    else:
        return redirect(owner_login)


def delete_category(request,id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        category = Category.objects.get(id=id)
        category.delete()
        return redirect(manage_category)
    else:
        return redirect(owner_login)