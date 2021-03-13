from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from . models import UserDetails,Playlist,PlaylistContent
from creator.models import Contents,Show,CreatorDeatails,Follows
from owner.models import Category
import json
from django.http import JsonResponse
from django.core import serializers

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
    if request.user.is_authenticated:
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
        return render(request, './consumer/Profile.html')
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
    return render(request, './consumer/Pricing.html')
    
#core Part
def homepage(request):
    shows = Show.objects.all()
    artists = CreatorDeatails.objects.all()
    results = []
    try:
        followed_creators = Follows.objects.filter(followed=request.user,follow_type=True)
        for creators in followed_creators:
            followed_date = creators.date
            followed_time = creators.time
            show_notifications = Show.objects.filter(user=creators.creators.id).filter(date_of_published=followed_date) 
            creator_art = CreatorDeatails.objects.filter(user=creators.creators.id)     
            for i in show_notifications:
                results.append(i)
    except:
        followed_creators = []
    context = {'shows':shows,'artists':artists,'results':results}
    return render(request, './consumer/Home.html',context)

def consumer_latest_feed(request):
    data = {}
    category = Category.objects.all()
    for i in category:
        data[i.category_name] = Show.objects.filter(category=i)
    context = {'datas':data}
    return render(request, './consumer/Latest.html',context)

def category_view(request,id):
    shows = Show.objects.filter(category=id)
    category = Category.objects.get(id=id)
    context = {'shows':shows,'category':category}
    return render(request, './consumer/CategoryView.html',context)

def single_podcast(request,id):
    shows = Show.objects.get(id=id)
    episodes = Contents.objects.filter(show=shows)
    playlists = Playlist.objects.all()
    context = {'shows':shows,'episodes':episodes,'playlists':playlists}
    return render(request, './consumer/SinglePodcastShows.html',context)

def single_episode(request,id):
    episode = Contents.objects.get(id=id)
    playlists = Playlist.objects.filter(user=request.user)
    print(playlists)
    context = {'episode':episode,'playlists':playlists}
    return render(request, './consumer/SingleEpisodes.html',context)

def artists_list(request):
    artists = CreatorDeatails.objects.all()
    context = {'artists':artists}
    return render(request,'./consumer/ArtistsList.html',context)

def single_artist(request,id):
    artists = CreatorDeatails.objects.get(id=id)
    podcasts = Show.objects.filter(user=artists.user_id)
    followers = Follows.objects.filter(creators=artists.user_id,follow_type=True).count()
    context = {'artists':artists,'podcasts':podcasts,'creator_followers':followers}
    return render(request, './consumer/SingleArtistView.html',context)

def follow_podcaster(request,id):
    if request.method == 'POST':
        followType = request.POST['followType']
        artists = CreatorDeatails.objects.get(id=id)
        creator_id = User.objects.get(id=artists.user_id)

        if followType == 'follow':
            if Follows.objects.filter(followed=request.user.id,follow_type=True,creators=creator_id).exists():
                Follows.objects.get(followed=request.user.id,follow_type=True,creators=creator_id).delete()
                Follows.objects.create(creators=creator_id,followed=request.user,follow_type=False)
                return JsonResponse('unfollowed', safe=False)
            else:
                if Follows.objects.filter(followed=request.user.id,follow_type=False,creators=creator_id).exists():
                    Follows.objects.get(followed=request.user.id,follow_type=False,creators=creator_id).delete()
                    Follows.objects.create(creators=creator_id,followed=request.user,follow_type=True)
                else:
                    follows = Follows.objects.create(creators=creator_id,followed=request.user,follow_type=True)
                return JsonResponse('followed', safe=False)
        else:
            pass
    else:
        pass

def follow_show(request,id):
    if request.method == 'POST':
        followType = request.POST['followType']
        show = Show.objects.get(id=id)

        if followType == 'followpodcast':
            if Follows.objects.filter(followed=request.user.id,follow_type=True,show=show).exists():
                Follows.objects.get(followed=request.user.id,follow_type=True,show=show).delete()
                Follows.objects.create(show=show,followed=request.user,follow_type=False)
                return JsonResponse('unfollowed_show', safe=False)
            else:
                if Follows.objects.filter(followed=request.user.id,follow_type=False,show=show).exists():
                    Follows.objects.get(followed=request.user.id,follow_type=False,show=show).delete()
                    Follows.objects.create(show=show,followed=request.user,follow_type=True)
                else:
                    follows = Follows.objects.create(show=show,followed=request.user,follow_type=True)
                return JsonResponse('followed_show', safe=False)
        else:
            pass

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

def add_liked(request,id):
    consumer_data = Contents.objects.get(id=id)
    if request.method == 'POST':
        playlist_name = request.POST['playlistName']
    PlayList.objects.create(user=request.user,content=consumer_data,playlist_name=playlist_name)
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
        playlist_name = request.POST['playlistName']
        playlist = Playlist.objects.create(user=request.user,playlist_name=playlist_name)
        data = {'playlistcreated':serializers.serialize('json',[playlist])}
        return JsonResponse(data)
    else:
        return render(request, './consumer/CreatePlaylist.html')

def delete_playlist(request,id):
    playlist = Playlist.objects.filter(id=id,user=request.user)
    playlist.delete()
    return JsonResponse('playlistdeleted',safe=False)

def manage_playlist(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        if Playlist.objects.filter(user=request.user).exists():
            playlists = Playlist.objects.filter(user=request.user)
            for playlist in playlists:
                playlist_contents = PlaylistContent.objects.filter(playlist=playlist.id)
            count_of_playlist_items = playlist_contents.count()
        else:
            count_of_playlist_items = 0
            playlists = []
        context = {'playlists':playlists,'count_of_playlist_items':count_of_playlist_items}
        return render(request, './consumer/ManagePlaylist.html',context)
    else:
        return redirect(signin)

def manage_playlist_content(request,id):
    playlists = Playlist.objects.get(id=id)
    playlist_contents = PlaylistContent.objects.filter(playlist=playlists)
    print(playlist_contents)
    context = {'playlist_contents':playlist_contents,'playlists':playlists}
    return render(request, './consumer/PlaylistContents.html',context)

def remove_playlist_content(request,id):
    podcast = PlaylistContent.objects.get(id=id)
    podcast.delete()
    return JsonResponse('itemremoved',safe=False)

def consumer_playlist_data(request):
    liked_songs = Playlist.objects.filter(user=request.user)
    context = {'liked_songs':liked_songs}
    return render(request, './consumer/Playlists.html',context)
