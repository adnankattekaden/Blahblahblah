from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from . models import UserDetails,Playlist,PlaylistContent,Subscribtions,UserRating
from creator.models import Contents,Show,CreatorDeatails,Follows,FollowShows,EpisodeAnalytics
from owner.models import Category,Plans,Advertisement
import json
from django.http import JsonResponse
from django.core import serializers
from datetime import date
import uuid

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
            image = request.FILES['profile_image']
            email = request.POST['email']
            mobile_number = request.POST['mobile_number']

            user_primarydetails.first_name = first_name
            user_primarydetails.last_name = last_name
            user_primarydetails.email = email
            user_details.mobile_number = mobile_number
            user_details.image = image
            user_primarydetails.save()
            user_details.save()
            return JsonResponse('profileupdated', safe=False)
        else:
            context = {'user_details':user_details}
            return render(request, './consumer/EditProfile.html',context)
    else:
        return redirect(signin)

def faq(request):
    return render(request, './consumer/faq.html')

def pricing(request):
    plans = Plans.objects.all()
    context = {'plans':plans}
    return render(request, './consumer/Pricing.html',context)


def checkout(request):
    if request.method == 'POST':
        print(request)
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
    return render(request, './consumer/upgrade.html')
    
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
    shows = Show.objects.all()
    artists = CreatorDeatails.objects.all()
    #notifcaion starts
    results = []
    try:
        user_details = UserDetails.objects.get(user=request.user)
        followed_creators = Follows.objects.filter(followed=request.user,follow_type=True)
        for creators in followed_creators:
            followed_date = creators.date
            followed_time = creators.time
            show_notifications = Show.objects.filter(user=creators.creators.id,date_of_published__gte=creators.date,time_of_published__gte=followed_time)
            for i in show_notifications:
                results.append(i)
    except:
        followed_creators = []
        user_details = []
    notification_count = len(results)
    #notification Ends
    context = {'shows':shows,'artists':artists,'results':results,'user_details':user_details,'notification_count':notification_count}
    return render(request, './consumer/Home.html',context)

def latest_feeds(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        
        user_details = UserDetails.objects.get(user=request.user)
        latest_feeds = []

        for feed_show in FollowShows.objects.filter(followed=request.user,follow_type=True):
            feeds = Show.objects.filter(user_id=feed_show.show.user.id)
            followed_shows = []
            for j in feeds:
                followed_shows.append(j)
            
            for show in followed_shows:
                latest_feeds.append(show)
                
        #main starts here
        data = {}
        for i in latest_feeds:
            data[i] = Contents.objects.filter(show=i.id)
        context = {'followed_shows':latest_feeds,'datas':data,'user_details':user_details}
        return render(request, './consumer/Latest.html',context)
    else:
        return redirect(signin)

def category_feed(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        #notification starts
        results = []
        try:
            user_details = UserDetails.objects.get(user=request.user)
            followed_creators = Follows.objects.filter(followed=request.user,follow_type=True)
            for creators in followed_creators:
                followed_date = creators.date
                followed_time = creators.time
                show_notifications = Show.objects.filter(user=creators.creators.id,date_of_published__gte=creators.date,time_of_published__gte=followed_time)
                for i in show_notifications:
                    results.append(i)
        except:
            followed_creators = []
            user_details = []
        notification_count = len(results)
        #notification ends here
        data = {}
        category = Category.objects.all()
        for i in category:
            data[i] = Show.objects.filter(category=i)
        
        context = {'datas':data,'results':results,'notification_count':notification_count}
        return render(request, './consumer/CategoryFeeds.html',context)
    else:
        return redirect(signin)

def category_view(request,id):
    if request.user.is_authenticated and request.user.is_staff == False:
        #notification starts
        results = []
        try:
            user_details = UserDetails.objects.get(user=request.user)
            followed_creators = Follows.objects.filter(followed=request.user,follow_type=True)
            for creators in followed_creators:
                followed_date = creators.date
                followed_time = creators.time
                show_notifications = Show.objects.filter(user=creators.creators.id,date_of_published__gte=creators.date,time_of_published__gte=followed_time)
                for i in show_notifications:
                    results.append(i)
        except:
            followed_creators = []
            user_details = []
        notification_count = len(results)
        #notification ends here
        shows = Show.objects.filter(category=id)
        category = Category.objects.get(id=id)
        context = {'shows':shows,'category':category,'user_details':user_details,'notification_count':notification_count}
        return render(request, './consumer/CategoryView.html',context)
    else:
        return redirect(signin)

def single_podcast(request,id):
    if request.user.is_authenticated and request.user.is_staff == False:
        #notification starts
        results = []
        try:
            user_details = UserDetails.objects.get(user=request.user)
            followed_creators = Follows.objects.filter(followed=request.user,follow_type=True)
            for creators in followed_creators:
                followed_date = creators.date
                followed_time = creators.time
                show_notifications = Show.objects.filter(user=creators.creators.id,date_of_published__gte=creators.date,time_of_published__gte=followed_time)
                for i in show_notifications:
                    results.append(i)
        except:
            followed_creators = []
            user_details = []
        notification_count = len(results)
        #notification ends here
        shows = Show.objects.get(id=id)
        episodes = Contents.objects.filter(show=shows)
        playlists = Playlist.objects.all()

        try:
            follow_status = FollowShows.objects.get(show=shows.id).follow_status
        except:
            follow_status = []

        context = {'shows':shows,'episodes':episodes,'playlists':playlists,'follow_status':follow_status,'user_details':user_details,'notification_count':notification_count}
        return render(request, './consumer/SinglePodcastShows.html',context)
    else:
        return redirect(signin)

def single_episode(request,id):
    if request.user.is_authenticated and request.user.is_staff == False:
        #notification starts
        results = []
        try:
            user_details = UserDetails.objects.get(user=request.user)
            followed_creators = Follows.objects.filter(followed=request.user,follow_type=True)
            for creators in followed_creators:
                followed_date = creators.date
                followed_time = creators.time
                show_notifications = Show.objects.filter(user=creators.creators.id,date_of_published__gte=creators.date,time_of_published__gte=followed_time)
                for i in show_notifications:
                    results.append(i)
        except:
            followed_creators = []
            user_details = []
        notification_count = len(results)
        #notification ends here

        episode = Contents.objects.get(id=id)
        playlists = Playlist.objects.filter(user=request.user)

        try:
            user_rating = UserRating.objects.get(user=request.user,content=episode)
        except:
            user_rating = 0

        ads = Advertisement.objects.all()

        context = {'episode':episode,'playlists':playlists,'advertisment':ads,
        'user_details':user_details,'notification_count':notification_count,
        'user_rating':user_rating}
        return render(request, './consumer/SingleEpisodes.html',context)
    else:
        return redirect(signin)

def artists_list(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        #notification starts
        results = []
        try:
            user_details = UserDetails.objects.get(user=request.user)
            followed_creators = Follows.objects.filter(followed=request.user,follow_type=True)
            for creators in followed_creators:
                followed_date = creators.date
                followed_time = creators.time
                show_notifications = Show.objects.filter(user=creators.creators.id,date_of_published__gte=creators.date,time_of_published__gte=followed_time)
                for i in show_notifications:
                    results.append(i)
        except:
            followed_creators = []
            user_details = []
        notification_count = len(results)
        #notification ends here
        artists = CreatorDeatails.objects.all()
        context = {'artists':artists,'user_details':user_details,'notification_count':notification_count}
        return render(request,'./consumer/ArtistsList.html',context)
    else:
        return redirect(signin)

def single_artist(request,id):
    if request.user.is_authenticated and request.user.is_staff == False:
        #notification starts
        results = []
        try:
            user_details = UserDetails.objects.get(user=request.user)
            followed_creators = Follows.objects.filter(followed=request.user,follow_type=True)
            for creators in followed_creators:
                followed_date = creators.date
                followed_time = creators.time
                show_notifications = Show.objects.filter(user=creators.creators.id,date_of_published__gte=creators.date,time_of_published__gte=followed_time)
                for i in show_notifications:
                    results.append(i)
        except:
            followed_creators = []
            user_details = []
        notification_count = len(results)
        #notification ends here
        artists = CreatorDeatails.objects.get(id=id)
        podcasts = Show.objects.filter(user=artists.user_id)
        followers_count = Follows.objects.filter(creators=artists.user_id,follow_type=True).count()
        try:
            follow_status = Follows.objects.get(creators=artists.user.id).follow_status
        except:
            follow_status = []
        context = {'artists':artists,'podcasts':podcasts,'creator_followers_count':followers_count,'follow_status':follow_status,'user_details':user_details,'notification_count':notification_count}
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
            show = Show.objects.get(id=id)

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
    print(id)
    consumer_data = Contents.objects.filter(id__gt=id).order_by('id').first()
    if consumer_data is None:
        consumer_data = Contents.objects.all().order_by('id').first()
    print(consumer_data)
    data = {'next_songs':serializers.serialize('json',[consumer_data])}
    return JsonResponse(data)

def previous_music_data(request,id):
    consumer_data = Contents.objects.filter(id__lt=id).order_by('id').last()
    if consumer_data is None:
        consumer_data = Contents.objects.all().order_by('id').last()
    print(consumer_data)
    data = {'previous_songs':serializers.serialize('json',[consumer_data])}
    return JsonResponse(data)

def current_music_data(request,id):
    consumer_data = Contents.objects.get(id=id)
    data = {'current_song':serializers.serialize('json',[consumer_data])}
    return JsonResponse(data)

def music_listen_update(request,id):
    consumer_data = Contents.objects.get(id=id)
    update_listners = consumer_data.listeners + 1
    consumer_data.listeners = update_listners
    consumer_data.save()
    current_date = date.today()

    if EpisodeAnalytics.objects.filter(episodes_id=consumer_data.id,date=current_date).exists():
        user_listen_data = EpisodeAnalytics.objects.get(episodes=consumer_data,date=current_date)
        user_listen_data.listners = update_listners
        user_listen_data.save()
    else:
        print('heyyy')
        EpisodeAnalytics.objects.create(episodes=consumer_data,listners=update_listners)
    return JsonResponse('listner_updated', safe=False)

def add_liked(request,id):
    consumer_data = Contents.objects.get(id=id)
    if request.method == 'POST':
        playlist_name = request.POST['playlistName']

    like_songs = Playlist.objects.get(playlist_name='likedsong',user=request.user)
    if Playlist.objects.filter(user=request.user,playlist_name='likedsong').exists():
        # like_songs = Playlist.objects.get(playlist_name='likedsong',user=request.user)
        if PlaylistContent.objects.filter(playlist=like_songs,content=consumer_data,user=request.user).exists():
            PlaylistContent.objects.get(playlist=like_songs,content=consumer_data,user=request.user).delete()
            consumer_data.favorites = False
            consumer_data.save()
            return JsonResponse('removeLiked',safe=False)
        else:
            PlaylistContent.objects.create(playlist=like_songs,content=consumer_data,user=request.user)
            consumer_data.favorites = True
            consumer_data.save()
    else:
        Playlist.objects.create(user=request.user,playlist_name=playlist_name)
        PlaylistContent.objects.create(playlist=like_songs,content=consumer_data,user=request.user)
        print('heyy')
        consumer_data.favorites = True
        consumer_data.save()
    return JsonResponse('addedliked', safe=False)

def add_playlist(request,id):
    if request.method == 'POST':
        playlists_id = request.POST['playlistName']
        podcast = request.POST['podcastId']
        playlist_id = Playlist.objects.get(id=playlists_id)
        content_id = Contents.objects.get(id=podcast)
        PlaylistContent.objects.create(playlist=playlist_id,content=content_id)
    return JsonResponse('playlistadded',safe=False)

def create_playlist(request):
    if request.method == 'POST':
        #notification starts
        results = []
        try:
            user_details = UserDetails.objects.get(user=request.user)
            followed_creators = Follows.objects.filter(followed=request.user,follow_type=True)
            for creators in followed_creators:
                followed_date = creators.date
                followed_time = creators.time
                show_notifications = Show.objects.filter(user=creators.creators.id,date_of_published__gte=creators.date,time_of_published__gte=followed_time)
                for i in show_notifications:
                    results.append(i)
        except:
            followed_creators = []
            user_details = []
        notification_count = len(results)
        #notification ends here
        playlist_name = request.POST['playlistName']
        playlist = Playlist.objects.create(user=request.user,playlist_name=playlist_name)
        data = {'playlistcreated':serializers.serialize('json',[playlist])}
        return JsonResponse(data)
    else:
        context = {'user_details':user_details}
        return render(request, './consumer/CreatePlaylist.html',context)

def delete_playlist(request,id):
    playlist = Playlist.objects.filter(id=id,user=request.user)
    playlist.delete()
    return JsonResponse('playlistdeleted',safe=False)

def manage_playlist(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        #notification starts
        results = []
        try:
            user_details = UserDetails.objects.get(user=request.user)
            followed_creators = Follows.objects.filter(followed=request.user,follow_type=True)
            for creators in followed_creators:
                followed_date = creators.date
                followed_time = creators.time
                show_notifications = Show.objects.filter(user=creators.creators.id,date_of_published__gte=creators.date,time_of_published__gte=followed_time)
                for i in show_notifications:
                    results.append(i)
        except:
            followed_creators = []
            user_details = []
        notification_count = len(results)
        #notification ends here
        if Playlist.objects.filter(user=request.user).exists():
            playlists = Playlist.objects.filter(user=request.user).exclude(playlist_name='likedsong')
            for playlist in playlists:
                playlist_contents = PlaylistContent.objects.filter(playlist=playlist.id)
            try:
                count_of_playlist_items = playlist_contents.count()
            except:
                count_of_playlist_items = 0
        else:
            count_of_playlist_items = 0
            playlists = []
        context = {'playlists':playlists,'count_of_playlist_items':count_of_playlist_items,'user_details':user_details,'notification_count':notification_count}
        return render(request, './consumer/ManagePlaylist.html',context)
    else:
        return redirect(signin)

def manage_playlist_content(request,id):
    #notification starts
    results = []
    try:
        user_details = UserDetails.objects.get(user=request.user)
        followed_creators = Follows.objects.filter(followed=request.user,follow_type=True)
        for creators in followed_creators:
            followed_date = creators.date
            followed_time = creators.time
            show_notifications = Show.objects.filter(user=creators.creators.id,date_of_published__gte=creators.date,time_of_published__gte=followed_time)
            for i in show_notifications:
                results.append(i)
    except:
        followed_creators = []
        user_details = []
    notification_count = len(results)
    #notification ends here
    playlists = Playlist.objects.get(id=id)
    playlist_contents = PlaylistContent.objects.filter(playlist=playlists)
    context = {'playlist_contents':playlist_contents,'playlists':playlists,'user_details':user_details,'notification_count':notification_count}
    return render(request, './consumer/PlaylistContents.html',context)

def remove_playlist_content(request,id):
    podcast = PlaylistContent.objects.get(id=id)
    podcast.delete()
    return JsonResponse('itemremoved',safe=False)

def consumer_liked_data(request):
    liked_songs = Playlist.objects.get(user=request.user,playlist_name='likedsong')
    liked_contents = PlaylistContent.objects.filter(playlist=liked_songs)
    user_details = UserDetails.objects.get(user=request.user)
    context = {'liked_songs':liked_songs,'user_details':user_details,'liked_contents':liked_contents}
    return render(request, './consumer/LikedPlaylists.html',context)

def rating(request,id):
    if request.method == "POST":
        rating_value = request.POST['rating']
        content_id = Contents.objects.get(id=id)

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

        rate = Contents.objects.get(id=id)
        rate.rating = global_rating/5
        rate.save()
    return JsonResponse('rated',safe=False)