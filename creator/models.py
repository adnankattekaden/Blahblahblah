from django.db import models
from django.contrib.auth.models import User,auth
from owner.models import Category

# Create your models here.

class CreatorDeatails(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    about_me = models.CharField(max_length=255,null=True,blank=True)
    mobile_number = models.BigIntegerField(null=True,blank=True)
    role = models.CharField(default='Podcaster',max_length=255)
    image = models.FileField(upload_to='creatorprofile/')

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = '/static/creator/images/users/avatar-1.jpg'
        return url
    
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

class Show(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    show_name = models.CharField(max_length=200,null=True,blank=True)
    description = models.CharField(max_length=20000,null=True,blank=True)
    total_episodes = models.IntegerField(default=0,null=True,blank=True)
    date_of_published = models.DateField(auto_now_add=True,null=True,blank=True)
    time_of_published = models.TimeField(auto_now_add=True,null=True,blank=True)
    thumbnail = models.FileField(upload_to='showthumbnail/')
    host = models.CharField(max_length=255,null=True,blank=True)
    visiblity = models.CharField(max_length=20,null=True,blank=True)


    @property
    def ImageURL(self):
        try:
            url = self.thumbnail.url
        except:
            url = ''
        return url
    
    def delete(self, *args, **kwargs):
        self.thumbnail.delete()
        super().delete(*args, **kwargs)




class Contents(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    artist = models.CharField(max_length=255,null=True,blank=True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE,null=True)
    episode_name = models.CharField(max_length=255,null=True,blank=True)
    description = models.CharField(max_length=20000,null=True,blank=True)
    created_date = models.DateField(auto_now_add=True,null=True,blank=True)
    created_time = models.TimeField(auto_now_add=True,null=True,blank=True)
    date_of_published = models.DateField(null=True,blank=True)
    time_of_published = models.TimeField(null=True,blank=True)
    listeners = models.IntegerField(default=0)
    podcast = models.FileField(upload_to='podcasts/')
    thumbnail = models.FileField(upload_to='thumbnail/')
    rating = models.FloatField(default=0)
    visiblity = models.CharField(max_length=20,null=True,blank=True)


    @property
    def ImageURL(self):
        try:
            url = self.thumbnail.url
        except:
            url = ''
        return url
        

    @property
    def PodcastURL(self):
        try:
            url = self.podcast.url
        except:
            url = ''
        return url

    def delete(self, *args, **kwargs):
        self.podcast.delete()
        self.thumbnail.delete()
        super().delete(*args, **kwargs)


class EpisodeAnalytics(models.Model):
    episodes = models.ForeignKey(Contents,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    time = models.TimeField(auto_now_add=True,null=True,blank=True)
    listners = models.IntegerField(default=0,null=True,blank=True)

class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    episodes = models.ForeignKey(Contents,on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20,null=True,blank=True)
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    time = models.TimeField(auto_now_add=True,null=True,blank=True)

class Follows(models.Model):
    creators = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name='follow_follower')
    followed = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name='follow_followed')
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    time = models.TimeField(auto_now_add=True,null=True,blank=True)
    follow_type = models.BooleanField(null=True,blank=True)
    follow_status = models.CharField(null=True,blank=True,max_length=40)


class FollowShows(models.Model):
    creators = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name='follow_shows')
    followed = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name='followed_shows')
    show = models.ForeignKey(Show, on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    time = models.TimeField(auto_now_add=True,null=True,blank=True)
    follow_type = models.BooleanField(null=True,blank=True)
    follow_status = models.CharField(null=True,blank=True,max_length=40)