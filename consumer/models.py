from django.db import models
from django.contrib.auth.models import User,auth
from creator.models import Contents

# Create your models here.
class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.BigIntegerField(null=True,blank=True)
    image = models.FileField(upload_to='usersprofile/')
    premium = models.BooleanField(default=False)

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = '/static/consumer/images/user/11.png'
        return url
    
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    playlist_name = models.CharField(max_length=200,null=True,blank=True)

class PlaylistContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE,null=True,blank=True)
    content = models.ForeignKey(Contents, on_delete=models.CASCADE,null=True,blank=True)
    types = models.BooleanField(default=False)

class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    content = models.ForeignKey(Contents, on_delete=models.CASCADE,null=True)
    rating = models.FloatField()


class Subscribtions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    plan_name = models.CharField(max_length=200)
    validity = models.IntegerField()
    price = models.FloatField()
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)