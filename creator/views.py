from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
import json
from django.http import JsonResponse
from .models import Contents,CreatorDeatails,Show,Follows,EpisodeAnalytics
from owner.models import Category
from django.views.decorators.csrf import csrf_exempt
import base64
from django.core.files.base import ContentFile
from datetime import date
import datetime 

# Create your views here.

def creator_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        verifypassword = request.POST['verifypassword']
        mobile_number = request.POST['mobile_number']

        if password==verifypassword:
            if User.objects.filter(email=email).exists():
                return JsonResponse('emailtaken', safe=False)
            elif User.objects.filter(username=username).exists():
                JsonResponse('usernametaken',safe=False)
            elif CreatorDeatails.objects.filter(mobile_number=mobile_number).exists():
                JsonResponse('mobilenumbertaken',safe=False)
            else:
                user = User.objects.create_user(email=email,username=username,password=password,is_staff=True)
                CreatorDeatails.objects.create(user=user,mobile_number=mobile_number)
                return JsonResponse('success',safe=False)
        else:
            return JsonResponse('invalidpassword',safe=False)
    else:
        return render(request, './creator/Signup.html')

def creator_login(request):
    if request.user.is_authenticated and request.user.is_staff == True:
        return redirect(creator_dashboard)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if not user.is_staff == False:
            if user:
                auth.login(request,user)
                return JsonResponse('loginsucess', safe=False)
            else:
                return JsonResponse('loginfail', safe=False)
        else:
            return JsonResponse('youarenotcreator', safe=False)
    else:
        return render(request, './creator/Login.html')

def creator_logout(request):
    auth.logout(request)
    return redirect(creator_login)

def creator_dashboard(request):
    if request.user.is_authenticated and request.user.is_staff == True:
        creator = CreatorDeatails.objects.get(user=request.user)
        followers_count = Follows.objects.filter(creators=request.user,follow_type=True).count()
        shows_count = Show.objects.filter(user=request.user).count()
        context = {'creator_details':creator,'shows_count':shows_count,'followers_count':followers_count}
        return render(request, './creator/Dashboard.html',context)
    else:
        return redirect(creator_login)
#creator
def creator_profile(request):
    if request.user.is_authenticated and request.user.is_staff == True:
        creator = CreatorDeatails.objects.get(user=request.user)
        user = User.objects.get(id=request.user.id)
        shows_count = Show.objects.filter(user=request.user).count()
        followers = Follows.objects.filter(creators=request.user,follow_type=True).count()
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            about_me = request.POST['about_me']
            image = request.FILES.get('profile_image')

            user.first_name = first_name
            user.last_name = last_name
            creator.about_me = about_me
            creator.image = image
            creator.save()
            user.save()
            return JsonResponse('profile_created',safe=False)
        else:
            context = {'creator_details':creator,'creator_followers':followers,'shows_count':shows_count}
            return render(request, './creator/Profile.html',context)
    else:
        return redirect(creator_login)

def edit_profile(request,id):
    if request.user.is_authenticated and request.user.is_staff == True:
        creator_details = CreatorDeatails.objects.get(user=id)
        context = {'creator_details':creator_details}
        return render(request,'./creator/EditProfile.html',context)
    else:
        return redirect(creator_login)
        
def edit_profiles(request,id):
    if request.method == 'POST':
        creator_primary_details = User.objects.get(id=id)
        creator_details = CreatorDeatails.objects.get(user=id)
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile_number = request.POST['mobile']
        about_me = request.POST['about_me']
        image = request.FILES.get('profile_image')

        creator_primary_details.first_name = first_name
        creator_primary_details.last_name = last_name
        creator_primary_details.email = email
        creator_details.mobile_number = mobile_number
        creator_details.about_me = about_me

        if image is not None:
            creator_details.image = image

        creator_primary_details.save()
        creator_details.save()
    return JsonResponse('profileedited',safe=False)

#contents
def manage_podcasts(request):
    if request.user.is_authenticated and request.user.is_staff == True:
        creator = CreatorDeatails.objects.get(user=request.user)
        shows = Show.objects.filter(user=request.user)
        context = {'shows':shows,'creator_details':creator}
        return render(request, './creator/ManagePodcasts.html',context)
    else:
        return redirect(creator_login)

def create_podcast(request):
    if request.user.is_authenticated and request.user.is_staff == True:
        creator = CreatorDeatails.objects.get(user=request.user)
        categories = Category.objects.all()
        if request.method == 'POST':
            podcast_name = request.POST['podcastName']
            category_id = request.POST['category']
            thumbnail = request.FILES.get('thumbnail')
            show_description = request.POST['showdescription']
            Show.objects.create(show_name=podcast_name,category_id=category_id,user=request.user,thumbnail=thumbnail,description=show_description,host=request.user)
            return JsonResponse('podcastcreated',safe=False)
        else:
            context = {'categories':categories,'creator_details':creator}
            return render(request, './creator/CreatePodacasts.html',context)
    else:
        return redirect(creator_login)

def edit_podcast(request,id):
    if request.user.is_authenticated and request.user.is_staff == True:
        categories = Category.objects.all()
        podcast_show = Show.objects.get(id=id)
        creator = CreatorDeatails.objects.get(user=request.user)
        if request.method == 'POST':
            thumbnail = request.FILES.get('thumbnail')
            podcast_show.show_name = request.POST['podcastName']
            podcast_show.category_id = request.POST['category']

            if thumbnail is not None:
                podcast_show.thumbnail = request.FILES.get('thumbnail')

            podcast_show.save()
            return JsonResponse('podcast_edited',safe=False)
        else:
            context = {'podcast_show':podcast_show,'creator_details':creator}
            return render(request, './creator/EditPodcasts.html',context)
    else:
        return redirect(creator_login)

def delete_podcast(request,id):
    if request.user.is_authenticated and request.user.is_staff == True:
        podcast = Show.objects.get(id=id)
        podcast.delete()
        return redirect(manage_podcasts)
    else:
        return redirect(creator_login)

def manage_episodes(request,id):
    if request.user.is_authenticated and request.user.is_staff == True:
        creator = CreatorDeatails.objects.get(user=request.user)
        show = Show.objects.get(id=id)
        episodes = Contents.objects.filter(user=request.user,show=show)
        context = {'episodes':episodes,'creator_details':creator}
        return render(request, './creator/MangeEpisodes.html',context)
    else:
        return redirect(creator_login)

def create_episode(request):
    if request.user.is_authenticated and request.user.is_staff == True:
        creator = CreatorDeatails.objects.get(user=request.user)
        shows = Show.objects.filter(user=request.user)
        if request.method == 'POST':
            episode_name = request.POST['episodeName']
            episode_art = request.FILES.get('episodeart')
            episode_description = request.POST['description']
            show_id = request.POST['show']
            podcast_data = request.FILES.get('audio')
            Contents.objects.create(user=request.user,episode_name=episode_name,description=episode_description,show_id=show_id,podcast=podcast_data,thumbnail=episode_art,artist=request.user)
            return JsonResponse('episode_created',safe=False)
        else:
            context = {'shows':shows,'creator_details':creator}
            return render(request, './creator/CreateEpisodes.html',context)
    else:
        return redirect(creator_login)
    
def edit_episode(request,id):
    if request.user.is_authenticated and request.user.is_staff == True:
        creator = CreatorDeatails.objects.get(user=request.user)
        episode = Contents.objects.get(id=id)
        if request.method == 'POST':            
            episode_name = request.POST['episodeName']
            episode_art = request.FILES.get('episodeart')
            episode_description = request.POST['description']
            show_id = request.POST['show']
            podcast_data = request.FILES.get('audio')

            shows = Show.objects.get(id=show_id)
            episode.episode_name = episode_name

            if episode_art is not None:
                episode.thumbnail = episode_art
    
            episode.description = episode_description
            episode.show = shows

            if podcast_data is not None:
                episode.podcast = podcast_data
            
            episode.save()
            return JsonResponse('episode_edited',safe=False)
        else:
            context = {'episode':episode,'creator_details':creator}
            return render(request, './creator/EditEpisodes.html',context)
    else:
        return redirect(creator_login)

def delete_episode(request,id):
    if request.user.is_authenticated and request.user.is_staff == True:
        episode = Contents.objects.get(id=id)
        episode.delete()
        return redirect(manage_podcasts)
    else:
        return redirect(creator_login)

def episode_analytics(request,id):
    creator = CreatorDeatails.objects.get(user=request.user)
    episode = Contents.objects.get(id=id)
    if request.method == "POST":
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
    else:
        days = []
        current_date = date.today()
        yesterday = current_date - datetime.timedelta(days = 1)

        try:
            episode_analytics = EpisodeAnalytics.objects.get(episodes=episode.id,date=current_date)   
        except:
            episode_analytics = []
    #analytics data
    context = {'episode_analytics':episode_analytics,'creator_details':creator}
    return render(request, './creator/EpisodeAnalytics.html',context)


