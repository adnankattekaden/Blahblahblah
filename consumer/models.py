from django.db import models
from django.contrib.auth.models import User,auth
from creator.models import Contents

# Create your models here.
class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.BigIntegerField(null=True,blank=True)
    image = models.FileField(upload_to='usersprofile/')

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    playlist_name = models.CharField(max_length=200,null=True,blank=True)

class PlaylistContent(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE,null=True,blank=True)
    content = models.ForeignKey(Contents, on_delete=models.CASCADE,null=True,blank=True)
