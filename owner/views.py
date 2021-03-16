from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
import json
from django.http import JsonResponse
from owner.models import Category,Plans,Advertisement
from consumer.models import Subscribtions
from datetime import date

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
    #total_counts 
    total_creators_count = User.objects.filter(is_staff=True).count()
    total_listners_count = User.objects.filter(is_staff=False).count()
    #sales 
    current_date = date.today()
    subscribtions = Subscribtions.objects.filter(date=current_date)
    dict = {}
    sub_count = 0
    for report in subscribtions:
        sub_count = sub_count + 1
        if not report.date in dict.keys():
            dict[report.date] = report
            dict[report.date].totalsubs = sub_count
        else:
            dict[report.date].totalsubs = sub_count

    total_sales = sub_count
    context = {'total_creators_count':total_creators_count,'total_listners_count':total_listners_count,'total_sales':total_sales}
    return render(request, './owner/Dashboard.html',context)

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

def manage_plans(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        plans = Plans.objects.all()
        context = {'plans':plans}
        return render(request, './owner/ManagePlans.html',context)
    else:
        return redirect(owner_login)

def create_plan(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == 'POST':
            plan_name = request.POST['plan_name']
            plan_price = request.POST['plan_price']
            validity = request.POST['validity']
            Plans.objects.create(plan_name=plan_name,price=plan_price,validity=validity)
            return JsonResponse('plancreated', safe=False)
        else:
            return render(request, './owner/CreatePlans.html')
    else:
        return redirect(owner_login)

def delete_plan(request,id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        plan = Plans.objects.get(id=id)
        plan.delete()
        return JsonResponse('plan_deleted', safe=False)
    else:
        return redirect(owner_login)

def manage_ads(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        ads = Advertisement.objects.all()
        context = {'advertisements':ads}
        return render(request, './owner/ManageAds.html',context)
    else:
        return redirect(owner_login)
    
def create_ads(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == "POST":
            ad_name = request.POST['advertisement_name']
            ad_image = request.FILES.get('advertisement_image')
            Advertisement.objects.create(ad_name=ad_name,ad_image=ad_image)
            return JsonResponse('ad_created', safe=False)
        else:
            return render(request, './owner/CreateAds.html')
    else:
        return redirect(owner_login)

def sales_report(request):
    current_date = date.today()
    subscribtions = Subscribtions.objects.filter(date=current_date)
    dict = {}
    count = 1
    sub_count = 0
    for report in subscribtions:
        sub_count = sub_count + 1
        if not report.date in dict.keys():
            dict[report.date] = report
            dict[report.date].price = report.price
            dict[report.date].totalsubs = sub_count
        else:
            dict[report.date].price += report.price
            dict[report.date].totalsubs = sub_count

    context = {'subscribtions':subscribtions,'dict':dict}
    return render(request, './owner/subsrcription_SalesReport.html',context)

def cancelled_report(request):
    return render(request, './owner/subscription_CancelledReport.html')
