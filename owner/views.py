from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
import json
from django.http import JsonResponse
from owner.models import Category,Plans,Advertisement,FeaturedShows,TopPodcasters,TrendingShows,PopularShows
from consumer.models import Subscribtions,UserDetails
from creator.models import Show,CreatorDeatails
import base64
from django.core.files.base import ContentFile
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
    total_creators_count = User.objects.filter(is_staff=True).exclude(is_superuser=True).count()
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

    #salesChart
    sales_data = [0,0,0,0,0,0,0,0,0,0,0,0]
    subscribtions_datas = Subscribtions.objects.all()
    for i in subscribtions_datas:
        sales_data[i.date.month-1] += 1

    #usersChart
    consumers_data = UserDetails.objects.all().count()
    creators_data = CreatorDeatails.objects.all().count()

    context = {'total_creators_count':total_creators_count,'total_listners_count':total_listners_count,'total_sales':total_sales,'sales_data':sales_data,'consumers_data':consumers_data,'creators_data':creators_data}
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
            return JsonResponse('edited_category',safe=False)
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
            ad_image = request.POST['advertisement_image']
            #imagecroping
            format, imgstr = ad_image.split(';base64,')
            ext = format.split('/')[-1]
            ad_image = ContentFile(base64.b64decode(imgstr), name=ad_name + '.' + ext)
            #corping Ends
            advertisementType = request.POST['AdvertisementType']
            Advertisement.objects.create(ad_name=ad_name,ad_image=ad_image,types=advertisementType)
            return JsonResponse('ad_created', safe=False)
        else:
            return render(request, './owner/CreateAds.html')
    else:
        return redirect(owner_login)

def delete_ads(request,id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        ad = Advertisement.objects.get(id=id).delete()
        return JsonResponse('ad_delete',safe=False)
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

def manage_listners(request):
    listners = User.objects.filter(is_staff=False)
    context = {'listners':listners}
    return render(request, './owner/ManageListners.html',context)

def manage_creators(request):
    creators = User.objects.filter(is_staff=True,is_superuser=False)
    context = {'creators':creators}
    return render(request, './owner/ManageCreators.html',context)

def block_users(request,id):
    if request.method == "GET":
        block_user = User.objects.get(id=id)
        block_user.is_active = False
        block_user.save()
    return JsonResponse('usrblocked',safe=False)

def unblock_users(request,id):
    if request.method == "GET":
        unblock_user = User.objects.get(id=id)
        unblock_user.is_active = True
        unblock_user.save()
    return JsonResponse('ublocked',safe=False)

#homePageSettings

def manage_featured_shows(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        featured_shows = FeaturedShows.objects.all()
        context = {'featured_shows':featured_shows}
        return render(request, './owner/FeaturedShows.html',context)
    else:
        return redirect(owner_login)

def add_featured_shows(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == "POST":
            showid = request.POST.getlist('addFeaturedShows')
            show = Show.objects.get(id=showid[0])
            FeaturedShows.objects.create(show=show)
            return redirect(manage_featured_shows)
        else:
            shows = Show.objects.all
            context = {'shows':shows}
            return render(request, './owner/AddFeaturedShow.html',context)
    else:
        return redirect(owner_login)

def remove_featured_show(request,id):
    if request.method == "GET":
        show = FeaturedShows.objects.get(show_id=id)
        show.delete()
    return JsonResponse('show_removed',safe=False)

def manage_top_podcasters(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        top_podcasters = TopPodcasters.objects.all()
        context = {'top_podcasters':top_podcasters}
        return render(request, './owner/ManageTopPodcasters.html',context)
    else:
        return redirect(owner_login)

def add_top_podcasters(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == "POST":
            artist_id = request.POST.get('addPodcasters')
            creators = CreatorDeatails.objects.get(id=artist_id)
            TopPodcasters.objects.create(creator=creators)
            return redirect(manage_top_podcasters)
        else:
            creators = CreatorDeatails.objects.all()
            context = {'creators':creators}
            return render(request, './owner/AddTopPodcasters.html',context)

def remove_top_podcasters(request,id):
    if request.method == "GET":
        artist = TopPodcasters.objects.get(creator=id)
        artist.delete()
    return JsonResponse('artist_removed',safe=False)

def manage_trending(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        trending_shows = TrendingShows.objects.all()
        context = {'trending_shows':trending_shows}
        return render(request, './owner/TrendingShows.html',context)
    else:
        return redirect(owner_login)

def add_trending(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == "POST":
            showid = request.POST.get('addFeaturedShows')
            show = Show.objects.get(id=showid)
            TrendingShows.objects.create(show=show)
            return redirect(manage_trending)
        else:
            shows = Show.objects.all
            context = {'shows':shows}
            return render(request, './owner/AddTrending.html',context)

def remove_trending(request,id):
    if request.method == "GET":
        trending = TrendingShows.objects.get(show_id=id)
        trending.delete()
    return JsonResponse('trending_removed',safe=False)

def manage_popular_shows(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        popular_shows = PopularShows.objects.all()
        context = {'popular_shows':popular_shows}
        return render(request, './owner/PopuplarShows.html',context)
    else:
        return redirect(owner_login)

def add_popular_shows(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == "POST":
            showid = request.POST.get('addpopularshows')
            show = Show.objects.get(id=showid)
            PopularShows.objects.create(show=show)
            return redirect(manage_popular_shows)
        else:
            shows = Show.objects.all
            context = {'shows':shows}
            return render(request, './owner/AddPopularShows.html',context)

def remove_popular_shows(request,id):
    if request.method == "GET":
        show = PopularShows.objects.get(show_id=id)
        show.delete()
    return JsonResponse('popular_show_removed',safe=False)