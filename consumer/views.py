from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from . models import UserDetails,Playlist,PlaylistContent,Subscribtions,UserRating
from creator.models import Contents,Show,CreatorDeatails,Follows,FollowShows,EpisodeAnalytics,Reaction
from owner.models import Category,Plans,Advertisement,FeaturedShows,TopPodcasters,TrendingShows,PopularShows
import json
from django.http import JsonResponse
from django.core import serializers
from datetime import date
import datetime 
from datetime import datetime
import uuid
import wave
import contextlib
import base64
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import check_password, make_password
import random



# Create your views here.

def signup(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        return redirect(homepage)

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        verify_password = request.POST['verify_password']

        if password == verify_password:
            if User.objects.filter(email=email).exists():
                return JsonResponse('emailtaken', safe=False)
            elif User.objects.filter(username=username).exists():
                return JsonResponse('usernametaken', safe=False)
            elif UserDetails.objects.filter(mobile_number=mobile_number).exists():
                return JsonResponse('mobilenumberexists', safe=False)
            else:
                user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                UserDetails.objects.create(user=user,mobile_number=mobile_number)
                return JsonResponse('success', safe=False)
        else:
            return JsonResponse('invalidpassword', safe=False)
    else:
        return render(request, './consumer/Signup.html')

def signin(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        return redirect(homepage)


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
        return render(request, './consumer/SignIn.html')

def signout(request):
    auth.logout(request)
    return redirect(signin)

#userProfile Part

def consumer_profile(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        followed_shows_count = FollowShows.objects.filter(followed=request.user,follow_type=True).count()
        followed_artists_count = Follows.objects.filter(followed=request.user,follow_type=True).count()
        user_details = UserDetails.objects.get(user=request.user)
        context = {'followed_shows_count':followed_shows_count,'followed_artists_count':followed_artists_count,'user_details':user_details}
        return render(request, './consumer/Profile.html',context)
    else:
        return redirect(signin)

def consumer_profile_edit(request,id):
    if request.user.is_authenticated and request.user.is_staff == False:
        user_primarydetails = User.objects.get(id=request.user.id)
        user_details = UserDetails.objects.get(user=id)
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            image = request.POST['profile_image']
            email = request.POST['email']
            mobile_number = request.POST['mobile_number']

            #imagecroping
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]
            profile_picture = ContentFile(base64.b64decode(imgstr), name=first_name + '.' + ext)
            #corping Ends

            user_primarydetails.first_name = first_name
            user_primarydetails.last_name = last_name
            user_primarydetails.email = email
            user_details.mobile_number = mobile_number
            user_details.image = profile_picture
            user_primarydetails.save()
            user_details.save()
            return JsonResponse('profileupdated', safe=False)
        else:
            context = {'user_details':user_details}
            return render(request, './consumer/EditProfile.html',context)
    else:
        return redirect(signin)

def change_password(request,id):
    user_details = User.objects.get(id=id)
    if request.method == "POST":
        check_user_password = check_password(request.POST['current_password'],request.user.password)
        new_password = request.POST['new_password']
        verify_password = request.POST['verify_password']
        if check_user_password:
            if new_password == verify_password:
                user_details.password = make_password(new_password)
                user_details.save()
                return JsonResponse('password_updated',safe=False)
            else:
                return JsonResponse('newpassword_not_matching')
        else:
            return JsonResponse('current_password_notmatching',safe=False)

def faq(request):
    return render(request, './consumer/faq.html')

def pricing(request):
    user_details = UserDetails.objects.get(user=request.user)
    plans = Plans.objects.all()
    context = {'plans':plans,'user_details':user_details}
    return render(request, './consumer/Pricing.html',context)

def checkout(request):
    if request.method == 'POST':
        plan_name = request.POST['planName']
        plan_price = request.POST['planPrice']
        plan_validity = request.POST['planValidity']
        myuuid = uuid.uuid4().hex[:8]
        transaction_id = 'ORDER' + str(myuuid)

        Subscribtions.objects.create(user=request.user,plan_name=plan_name,validity=plan_validity,price=plan_price,transaction_id=transaction_id,payment_status=True)
        premium = UserDetails.objects.get(user=request.user.id)
        premium.premium = True
        premium.save()
    return JsonResponse('upgraded', safe=False)

def recipts(request):
    recipts = Subscribtions.objects.filter(user=request.user)
    user_details = UserDetails.objects.get(user=request.user)
    context = {'recipts':recipts,'user_details':user_details}
    return render(request, './consumer/ReciptsList.html',context)


def invoice(request,id):
    invoice= Subscribtions.objects.get(id=id)
    user_details = UserDetails.objects.get(user=request.user)
    context = {'invoice':invoice,'user_details':user_details}
    return render(request, './consumer/Invoice.html',context)

def thankyou_note(request):
    user_details = UserDetails.objects.get(user=request.user)
    context = {'user_details':user_details}
    return render(request, './consumer/upgrade.html',context)
    
def followed_podcast_list(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        user_details = UserDetails.objects.get(user=request.user)
        shows = FollowShows.objects.filter(followed=request.user,follow_type=True)
        followed_shows = []
        for i in shows:
            followed_shows.append(i.show)
        context = {'followed_shows':followed_shows,'user_details':user_details}
        return render(request, './consumer/FollowedPodcastsList.html',context)
    else:
        return redirect(signin)

def followed_artists_list(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        user_details = UserDetails.objects.get(user=request.user)
        artists = Follows.objects.filter(followed=request.user,follow_type=True)
        followed_artists = []
        followed_creator_details = []

        for i in artists:
            followed_artists.append(i)

        for j in followed_artists:
            creator_detatils = CreatorDeatails.objects.filter(user=j.creators.id)
            for k in creator_detatils:
                followed_creator_details.append(k)

        context = {'followed_creator_details':followed_creator_details,'user_details':user_details}
        return render(request, './consumer/FollowedArtistsList.html',context)
    else:
        return redirect(signin)

#core Part
def homepage(request):
    shows = Show.objects.filter(visiblity="Public",user__is_active=True)
    artists = CreatorDeatails.objects.filter(user__is_active=True)

    top_podcasters = TopPodcasters.objects.all()
    fetaured_shows = FeaturedShows.objects.filter(show__visiblity="Public")
    trending_shows = TrendingShows.objects.filter(show__visiblity="Public")
    popular_shows = PopularShows.objects.filter(show__visiblity="Public")


    #notifcaion starts
    try:
        user_details = UserDetails.objects.get(user=request.user)
        latest_notificaions = []
        for feed_show in FollowShows.objects.filter(followed=request.user,follow_type=True):
            feeds = Show.objects.filter(user_id=feed_show.show.user.id,visiblity="Public")
            followed_shows = []
            for j in feeds:
                followed_shows.append(j)
            
            for show in followed_shows:
                latest_notificaions.append(show)

        #main starts here
        episode_notifications = {}
        for i in latest_notificaions:
            episode_notifications[i] = Contents.objects.filter(show=i.id,visiblity="Public")
            
    except:
        episode_notifications = 0
        user_details = []
        #notification Ends
    
    context = {'fetaured_shows':fetaured_shows,'top_podcasters':top_podcasters,'trending_shows':trending_shows,
    'popular_shows':popular_shows,'user_details':user_details,'datas':episode_notifications}
    return render(request, './consumer/Home.html',context)

def latest_feeds(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        
        user_details = UserDetails.objects.get(user=request.user)
        latest_feeds = []

        for feed_show in FollowShows.objects.filter(followed=request.user,follow_type=True):
            feeds = Show.objects.filter(user_id=feed_show.show.user.id,visiblity="Public")
            followed_shows = []
            for j in feeds:
                followed_shows.append(j)
            
            for show in followed_shows:
                latest_feeds.append(show)
                
        #main starts here
        data = {}
        for i in latest_feeds:
            data[i] = Contents.objects.filter(show=i.id,visiblity="Public")

        context = {'followed_shows':latest_feeds,'datas':data,'user_details':user_details}
        return render(request, './consumer/Latest.html',context)
    else:
        return redirect(signin)

def category_feed(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        #notifcaion starts
        user_details = UserDetails.objects.get(user=request.user)
        latest_notificaions = []
        for feed_show in FollowShows.objects.filter(followed=request.user,follow_type=True):
            feeds = Show.objects.filter(user_id=feed_show.show.user.id,visiblity="Public")
            followed_shows = []

            for j in feeds:
                followed_shows.append(j)
        
            for show in followed_shows:
                latest_notificaions.append(show)
        #main starts here
        episode_notifications = {}
        for i in latest_notificaions:
            episode_notifications[i] = Contents.objects.filter(show=i.id,visiblity="Public")
        #notification Ends

        #categoryStarts
        category_data = {}
        category = Category.objects.all()
        for i in category:
            category_data[i] = Show.objects.filter(category=i,visiblity="Public")
        
        context = {'category_data':category_data,'datas':episode_notifications,'user_details':user_details}
        return render(request, './consumer/CategoryFeeds.html',context)
    else:
        return redirect(signin)

def category_view(request,id):
    if request.user.is_authenticated and request.user.is_staff == False:

        #notifcaion starts
        user_details = UserDetails.objects.get(user=request.user)
        latest_notificaions = []

        for feed_show in FollowShows.objects.filter(followed=request.user,follow_type=True):
            feeds = Show.objects.filter(user_id=feed_show.show.user.id,visiblity="Public")
            followed_shows = []

            for j in feeds:
                followed_shows.append(j)
        
            for show in followed_shows:
                latest_notificaions.append(show)

        #main starts here
        episode_notifications = {}
        for i in latest_notificaions:
            episode_notifications[i] = Contents.objects.filter(show=i.id,visiblity="Public")
        #notification Ends

        shows = Show.objects.filter(category=id,visiblity="Public")
        category = Category.objects.get(id=id)
        context = {'shows':shows,'category':category,'user_details':user_details,'datas':episode_notifications}
        return render(request, './consumer/CategoryView.html',context)
    else:
        return redirect(signin)

def single_podcast(request,id):
    if request.user.is_authenticated and request.user.is_staff == False:
        #notifcaion starts
        try:
            user_details = UserDetails.objects.get(user=request.user)
            latest_notificaions = []

            for feed_show in FollowShows.objects.filter(followed=request.user,follow_type=True):
                feeds = Show.objects.filter(user_id=feed_show.show.user.id,visiblity="Public")
                followed_shows = []

                for j in feeds:
                    followed_shows.append(j)
            
                for show in followed_shows:
                    latest_notificaions.append(show)
        #main starts here

            episode_notifications = {}
            for i in latest_notificaions:
                episode_notifications[i] = Contents.objects.filter(show=i.id,visiblity="Public")
        except:
            episode_notifications = 0
        #notification Ends

        shows = Show.objects.get(id=id)
        episodes = Contents.objects.filter(show=shows,visiblity="Public",date_of_published__lte=date.today())
        total_episodes = 0
        for episode in episodes:
            total_episodes += 1
            
        playlists = Playlist.objects.all()

        try:
            follow_status = FollowShows.objects.get(show=shows.id).follow_status
        except:
            follow_status = []

        context = {'shows':shows,'episodes':episodes,'playlists':playlists,'follow_status':follow_status,'user_details':user_details,'datas':episode_notifications,'total_episodes':total_episodes}
        return render(request, './consumer/SinglePodcastShows.html',context)
    else:
        return redirect(signin)

def single_episode(request,id):
    if request.user.is_authenticated and request.user.is_staff == False:
        #notifcaion starts
        try:
            user_details = UserDetails.objects.get(user=request.user)
            latest_notificaions = []

            for feed_show in FollowShows.objects.filter(followed=request.user,follow_type=True):
                feeds = Show.objects.filter(user_id=feed_show.show.user.id,visiblity="Public")
                followed_shows = []

                for j in feeds:
                    followed_shows.append(j)
            
                for show in followed_shows:
                    latest_notificaions.append(show)
        #main starts here

            episode_notifications = {}
            for i in latest_notificaions:
                episode_notifications[i] = Contents.objects.filter(show=i.id,visiblity="Public")
        except:
            episode_notifications = 0
        #notification Ends

        episode = Contents.objects.get(id=id)
        playlists = Playlist.objects.filter(user=request.user)
        

        #reactions
        try:
            reaction_type = Reaction.objects.get(episodes=episode,user=request.user).reaction_type
        except:
            reaction_type = 0


        #rating
        try:
            user_rating = UserRating.objects.get(user=request.user,content=episode)
        except:
            user_rating = 0

        #favorites 
        try:
            favorites_id = Playlist.objects.get(user=request.user,playlist_name='Favorites')
        except:
            favorites_id = Playlist.objects.create(user=request.user,playlist_name='Favorites')

        if PlaylistContent.objects.filter(playlist=favorites_id.id,user=request.user,content=episode.id,types=True).exists():
            favorites_list = PlaylistContent.objects.get(playlist=favorites_id.id,user=request.user,content=episode.id,types=True)
        else:
            favorites_list = False
        
        #advertisment
        ad_list = []
        if Advertisement.objects.filter(types="banner").exists():
            ads = Advertisement.objects.filter(types="banner")
            for i in ads:
                ad_list.append(i)
            random_ad = random.choice(ad_list)

        #advertisment_ends
        context = {'episode':episode,'playlists':playlists,'advertisment':random_ad,
        'user_details':user_details,'datas':episode_notifications,
        'user_rating':user_rating,'favorites_list':favorites_list,'reaction_type':reaction_type}
        return render(request, './consumer/SingleEpisodes.html',context)
    else:
        return redirect(signin)

def artists_list(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        #notifcaion starts
        try:
            user_details = UserDetails.objects.get(user=request.user)
            latest_notificaions = []

            for feed_show in FollowShows.objects.filter(followed=request.user,follow_type=True):
                feeds = Show.objects.filter(user_id=feed_show.show.user.id,visiblity="Public")
                followed_shows = []

                for j in feeds:
                    followed_shows.append(j)
            
                for show in followed_shows:
                    latest_notificaions.append(show)
        #main starts here

            episode_notifications = {}
            for i in latest_notificaions:
                episode_notifications[i] = Contents.objects.filter(show=i.id,visiblity="Public")
        except:
            episode_notifications = 0
    #notification Ends

        artists = CreatorDeatails.objects.all()
        context = {'artists':artists,'user_details':user_details,'episode_notifications':episode_notifications}
        return render(request,'./consumer/ArtistsList.html',context)
    else:
        return redirect(signin)

def single_artist(request,id):
    if request.user.is_authenticated and request.user.is_staff == False:
        #notifcaion starts
        try:
            user_details = UserDetails.objects.get(user=request.user)
            latest_notificaions = []

            for feed_show in FollowShows.objects.filter(followed=request.user,follow_type=True):
                feeds = Show.objects.filter(user_id=feed_show.show.user.id,visiblity="Public")
                followed_shows = []

                for j in feeds:
                    followed_shows.append(j)
            
                for show in followed_shows:
                    latest_notificaions.append(show)
            #main starts here
            episode_notifications = {}
            for i in latest_notificaions:
                episode_notifications[i] = Contents.objects.filter(show=i.id,visiblity="Public")
        except:
            episode_notifications = 0
        #notification Ends
        
        artists = CreatorDeatails.objects.get(id=id)
        podcasts = Show.objects.filter(user=artists.user_id,visiblity="Public")

        shows_data = {}
        for show in podcasts:
            shows_data[show] = Contents.objects.filter(show=show).count()

        followers_count = Follows.objects.filter(creators=artists.user_id,follow_type=True).count()
        shows_count = podcasts.count()

        try:
            follow_status = Follows.objects.get(creators=artists.user.id,followed=request.user).follow_status
        except:
            follow_status = []

        context = {'artists':artists,'shows_data':shows_data,'creator_followers_count':followers_count,'follow_status':follow_status,'user_details':user_details,'data':episode_notifications,'shows_count':shows_count}
        return render(request, './consumer/SingleArtistView.html',context)
    else:
        return redirect(signin)

def follow_podcaster(request,id):
    if request.user.is_authenticated and request.user.is_staff == False:
        if request.method == 'POST':
            followType = request.POST['followType']
            artists = CreatorDeatails.objects.get(id=id)
            creator_id = User.objects.get(id=artists.user_id)

            if followType == 'follow':
                if Follows.objects.filter(followed=request.user.id,follow_type=True,creators=creator_id,follow_status='follow').exists():
                    Follows.objects.get(followed=request.user.id,follow_type=True,creators=creator_id,follow_status='follow').delete()
                    Follows.objects.create(creators=creator_id,followed=request.user,follow_type=False,follow_status='unfollow')
                    return JsonResponse('unfollowed', safe=False)
                else:
                    if Follows.objects.filter(followed=request.user.id,follow_type=False,creators=creator_id,follow_status='unfollow').exists():
                        Follows.objects.get(followed=request.user.id,follow_type=False,creators=creator_id,follow_status='unfollow').delete()
                        Follows.objects.create(creators=creator_id,followed=request.user,follow_type=True,follow_status='follow')
                    else:
                        follows = Follows.objects.create(creators=creator_id,followed=request.user,follow_type=True,follow_status='follow')
                    return JsonResponse('followed', safe=False)
            else:
                pass
        else:
            pass
    else:
        return redirect(signin)

def follow_show(request,id):
    if request.user.is_authenticated and request.user.is_staff == False:
        if request.method == 'POST':
            followType = request.POST['followType']
            show = Show.objects.get(id=id,visiblity="Public")

            if followType == 'followpodcast':
                if FollowShows.objects.filter(followed=request.user.id,follow_type=True,show=show,follow_status='follow').exists():
                    FollowShows.objects.get(followed=request.user.id,follow_type=True,show=show,follow_status='follow').delete()
                    FollowShows.objects.create(show=show,followed=request.user,follow_type=False,follow_status='unfollow')
                    return JsonResponse('unfollowed_show', safe=False)
                else:
                    if FollowShows.objects.filter(followed=request.user.id,follow_type=False,show=show,follow_status='unfollow').exists():
                        FollowShows.objects.get(followed=request.user.id,follow_type=False,show=show,follow_status='unfollow').delete()
                        FollowShows.objects.create(show=show,followed=request.user,follow_type=True,follow_status='follow')
                    else:
                        follows = FollowShows.objects.create(show=show,followed=request.user,follow_type=True,follow_status='follow')
                    return JsonResponse('followed_show', safe=False)
            else:
                pass
    else:
        return redirect(signin)

def next_music_data(request,id):
    show_id = Contents.objects.get(id=id)
    consumer_data = Contents.objects.filter(id__gt=id,visiblity="Public",show_id=show_id.show.id).order_by('id').first()
    if consumer_data is None:
        consumer_data = Contents.objects.filter(visiblity="Public",show_id=show_id.show.id).order_by('id').first()
    data = {'next_songs':serializers.serialize('json',[consumer_data])}
    return JsonResponse(data)

def previous_music_data(request,id):
    show_id = Contents.objects.get(id=id)
    consumer_data = Contents.objects.filter(id__lt=id,visiblity="Public",show_id=show_id.show.id).order_by('id').last()
    if consumer_data is None:
        consumer_data = Contents.objects.filter(visiblity="Public",show_id=show_id.show.id).order_by('id').last()
    data = {'previous_songs':serializers.serialize('json',[consumer_data])}
    return JsonResponse(data)

def current_music_data(request,id):
    consumer_data = Contents.objects.get(id=id,visiblity="Public")
    data = {'current_song':serializers.serialize('json',[consumer_data])}
    return JsonResponse(data)

def playfirst_show_music(request,id):
    show_id = Show.objects.get(id=id)
    consumer_data = Contents.objects.filter(visiblity="Public",show_id=show_id.id).first()
    data = {'playfirstshow_music':serializers.serialize('json',[consumer_data])}
    return JsonResponse(data,safe=False)

def music_listen_update(request,id):
    consumer_data = Contents.objects.get(id=id,visiblity="Public")
    update_listners = consumer_data.listeners + 1
    consumer_data.listeners = update_listners
    consumer_data.save()
    current_date = date.today()

    if EpisodeAnalytics.objects.filter(episodes_id=consumer_data.id,date=current_date).exists():
        user_listen_data = EpisodeAnalytics.objects.get(episodes=consumer_data,date=current_date)
        user_listen_data.listners = update_listners
        user_listen_data.save()
    else:
        EpisodeAnalytics.objects.create(episodes=consumer_data,listners=update_listners)
    return JsonResponse('listner_updated', safe=False)

def add_favorite(request,id):
    consumer_data = Contents.objects.get(id=id,visiblity="Public")
    if request.method == 'POST':
        playlist_name = request.POST['playlistName']
    
    like_songs,create_play = Playlist.objects.get_or_create(playlist_name=playlist_name,user=request.user)

    if Playlist.objects.filter(user=request.user,playlist_name=playlist_name).exists():
        if PlaylistContent.objects.filter(playlist=like_songs,content=consumer_data,user=request.user,types=True).exists():
            PlaylistContent.objects.get(playlist=like_songs,content=consumer_data,user=request.user,types=True).delete()
            return JsonResponse('removefavorites',safe=False)
        else:
            PlaylistContent.objects.create(playlist=like_songs,content=consumer_data,user=request.user,types=True)
    else:
        PlaylistContent.objects.create(playlist=like_songs,content=consumer_data,user=request.user,types=True)
    return JsonResponse('addedfavorites', safe=False)

def add_playlist(request,id):
    if request.method == 'POST':
        playlists_id = request.POST['playlistName']
        podcast = request.POST['podcastId']
        playlist_id = Playlist.objects.get(id=playlists_id)
        content_id = Contents.objects.get(id=podcast,visiblity="Public")
        PlaylistContent.objects.create(playlist=playlist_id,content=content_id)
    return JsonResponse('playlistadded',safe=False)

def create_playlist(request):
    if request.method == 'POST':
        playlist_name = request.POST['playlist_name']
        playlist = Playlist.objects.create(user=request.user,playlist_name=playlist_name)
        data = {'playlistcreated':serializers.serialize('json',[playlist])}
        return JsonResponse(data)
    else:
        #notifcaion starts
        try:
            user_details = UserDetails.objects.get(user=request.user)
            latest_notificaions = []

            for feed_show in FollowShows.objects.filter(followed=request.user,follow_type=True):
                feeds = Show.objects.filter(user_id=feed_show.show.user.id,visiblity="Public")
                followed_shows = []

                for j in feeds:
                    followed_shows.append(j)
            
                for show in followed_shows:
                    latest_notificaions.append(show)
        #main starts here

            episode_notifications = {}
            for i in latest_notificaions:
                episode_notifications[i] = Contents.objects.filter(show=i.id,visiblity="Public")
        except:
            episode_notifications = 0
    #notification Ends
        
        context = {'user_details':user_details,'datas':episode_notifications}
        return render(request, './consumer/CreatePlaylist.html',context)

def delete_playlist(request,id):
    playlist = Playlist.objects.filter(id=id,user=request.user)
    playlist.delete()
    return JsonResponse('playlistdeleted',safe=False)

def manage_playlist(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        #notifcaion starts
        try:
            user_details = UserDetails.objects.get(user=request.user)
            latest_notificaions = []

            for feed_show in FollowShows.objects.filter(followed=request.user,follow_type=True):
                feeds = Show.objects.filter(user_id=feed_show.show.user.id,visiblity="Public")
                followed_shows = []

                for j in feeds:
                    followed_shows.append(j)
            
                for show in followed_shows:
                    latest_notificaions.append(show)
        #main starts here

            episode_notifications = {}
            for i in latest_notificaions:
                episode_notifications[i] = Contents.objects.filter(show=i.id,visiblity="Public")
        except:
            episode_notifications = 0
        #notification Ends

        if Playlist.objects.filter(user=request.user).exists():
            playlists = Playlist.objects.filter(user=request.user).exclude(playlist_name='Favorites')
            playlist_data = {}
            for playlist in playlists:
                playlist_contents = PlaylistContent.objects.filter(playlist=playlist.id)
                playlist_data[playlist] = playlist_contents.count()
            favorites = Playlist.objects.filter(user=request.user,playlist_name='Favorites')
            for fav_id in favorites:
                liked_count = PlaylistContent.objects.filter(playlist=fav_id).count()

        else:
            playlists = []
            liked_count = 0
            playlist_data = 0

        context = {'playlists':playlists,'user_details':user_details,'datas':episode_notifications,'playlist_data':playlist_data,'liked_count':liked_count}
        return render(request, './consumer/ManagePlaylist.html',context)
    else:
        return redirect(signin)

def manage_playlist_content(request,id):
        #notifcaion starts
        try:
            user_details = UserDetails.objects.get(user=request.user)
            latest_notificaions = []

            for feed_show in FollowShows.objects.filter(followed=request.user,follow_type=True):
                feeds = Show.objects.filter(user_id=feed_show.show.user.id,visiblity="Public")
                followed_shows = []

                for j in feeds:
                    followed_shows.append(j)
            
                for show in followed_shows:
                    latest_notificaions.append(show)
            #main starts here

            episode_notifications = {}
            for i in latest_notificaions:
                episode_notifications[i] = Contents.objects.filter(show=i.id,visiblity="Public")
        except:
            episode_notifications = 0
        #notification Ends

        playlists = Playlist.objects.get(id=id)
        playlist_contents = PlaylistContent.objects.filter(playlist=playlists)
        context = {'playlist_contents':playlist_contents,'playlists':playlists,'user_details':user_details,'datas':episode_notifications}
        return render(request, './consumer/PlaylistContents.html',context)

def remove_playlist_content(request,id):
    podcast = PlaylistContent.objects.get(id=id)
    podcast.delete()
    return JsonResponse('itemremoved',safe=False)

def consumer_liked_data(request):
    #notifcaion starts
    try:
        user_details = UserDetails.objects.get(user=request.user)
        latest_notificaions = []

        for feed_show in FollowShows.objects.filter(followed=request.user,follow_type=True):
            feeds = Show.objects.filter(user_id=feed_show.show.user.id,visiblity="Public")
            followed_shows = []

            for j in feeds:
                followed_shows.append(j)
        
            for show in followed_shows:
                latest_notificaions.append(show)
        #main starts here

        episode_notifications = {}
        for i in latest_notificaions:
            episode_notifications[i] = Contents.objects.filter(show=i.id,visiblity="Public")
    except:
        episode_notifications = 0
    #notification Ends

    favorites,create = Playlist.objects.get_or_create(user=request.user,playlist_name='Favorites')
    favorite_contents = PlaylistContent.objects.filter(playlist=favorites)
    user_details = UserDetails.objects.get(user=request.user)
    context = {'user_details':user_details,'favorite_contents':favorite_contents,'datas':episode_notifications,'favorites':favorites}
    return render(request, './consumer/LikedPlaylists.html',context)

def rating(request,id):
    if request.method == "POST":
        rating_value = request.POST['rating']
        content_id = Contents.objects.get(id=id,visiblity="Public")

        #user rating
        if UserRating.objects.filter(user=request.user,content=content_id).exists():
            UserRating.objects.filter(user=request.user,content=content_id).delete()
        UserRating.objects.create(user=request.user,content=content_id,rating=rating_value)
        
        total_rating = []

        overall_content_rating = UserRating.objects.filter(content=content_id)
        for i in overall_content_rating:
            total_rating.append(float(i.rating))

        global_rating = 0
        for rating in total_rating:
            global_rating += rating

        rate = Contents.objects.get(id=id,visiblity="Public")
        rate.rating = global_rating/5
        rate.save()
    return JsonResponse('rated',safe=False)

def reaction(request,id):
    if request.method == "POST":
        reaction_type = request.POST['reaction_type']
        if reaction_type == "Like":
            episode_id = Contents.objects.get(id=id)
            if Reaction.objects.filter(user=request.user,episodes=episode_id,reaction_type=reaction_type).exists():
                Reaction.objects.filter(user=request.user,episodes=episode_id,reaction_type=reaction_type).delete()
                return JsonResponse('unlike',safe=False)
            elif Reaction.objects.filter(user=request.user,episodes=episode_id).exists():
                Reaction.objects.filter(user=request.user,episodes=episode_id).delete()
            else:
                Reaction.objects.create(user=request.user,episodes=episode_id,reaction_type=reaction_type)
            return JsonResponse('liked', safe=False)
        else:
            episode_id = Contents.objects.get(id=id)
            if Reaction.objects.filter(user=request.user,episodes=episode_id,reaction_type=reaction_type).exists():
                Reaction.objects.filter(user=request.user,episodes=episode_id,reaction_type=reaction_type).delete()
                return JsonResponse('undisike',safe=False)
            elif Reaction.objects.filter(user=request.user,episodes=episode_id).exists():
                Reaction.objects.filter(user=request.user,episodes=episode_id).delete()
                Reaction.objects.create(user=request.user,episodes=episode_id,reaction_type=reaction_type)
            else:
                Reaction.objects.create(user=request.user,episodes=episode_id,reaction_type=reaction_type)
            return JsonResponse('dislike', safe=False)

def search_box(request):
    serach_results = 0
    if request.method == "GET":
        showname = request.GET['showname']
        if Show.objects.filter(show_name__icontains=showname,visiblity="Public",user__is_active=True).exists():
            serach_results = 'nothing found'
        else:
            serach_results = Show.objects.filter(show_name__icontains=showname,visiblity="Public",user__is_active=True)

    context = {'serach_results':serach_results}
    return render(request, './consumer/search.html',context)

def your_library(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        user_details = UserDetails.objects.get(user=request.user)

        if FollowShows.objects.filter(followed=request.user,follow_type=True).exists():
            #following shows
            for followed_show in FollowShows.objects.filter(followed=request.user,follow_type=True):
                shows = Show.objects.filter(user_id=followed_show.show.user.id,visiblity="Public")
                followed_shows = []
                for i in shows:
                    followed_shows.append(i)
        else:
            followed_shows = []

        if Follows.objects.filter(followed=request.user,follow_type=True).exists():
            #following Artistts
            followed_artists = []
            for j in Follows.objects.filter(followed=request.user,follow_type=True):
                followed_artists.append(j)
            
            followed_creators = []
            for k in followed_artists:
                creator_detatils = CreatorDeatails.objects.filter(user=k.creators.id)
                for m in creator_detatils:
                    followed_creators.append(m)
        else:
            followed_creators = []

        context = {'user_details':user_details,'followed_creators':followed_creators,'followed_shows':followed_shows}
        return render(request, './consumer/YourLibrary.html',context)
    else:
        return redirect(signin)

def advertisment(request):
    ad_list = []
    if Advertisement.objects.filter(types="popup").exists():
        ads = Advertisement.objects.filter(types="popup")
        for i in ads:
            ad_list.append(i)
        random_ad = random.choice(ad_list)
        random_ad_data = {'random_ad':serializers.serialize('json',[random_ad])}
        return JsonResponse(random_ad_data)
    else:
        return JsonResponse('hey',safe=False)

def notifications(request):
    #notifcaion starts
        user_details = UserDetails.objects.get(user=request.user)
        latest_notificaions = []

        for feed_show in FollowShows.objects.filter(followed=request.user,follow_type=True):
            feeds = Show.objects.filter(user_id=feed_show.show.user.id,visiblity="Public")
            followed_shows = []

            for j in feeds:
                followed_shows.append(j)
        
            for show in followed_shows:
                latest_notificaions.append(show)
    #main starts here

        episode_notifications = {}
        for i in latest_notificaions:
            episode_notifications[i] = Contents.objects.filter(show=i.id,visiblity="Public")
        notification_alerts = {'episode_notifications':serializers.serialize('json',episode_notifications)}
        return JsonResponse(notification_alerts)
    #notification Ends