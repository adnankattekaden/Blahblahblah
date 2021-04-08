from django.db import models
from creator.models import *
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=255)

class Plans(models.Model):
    plan_name = models.CharField(max_length=255,null=True,blank=True)
    price = models.FloatField()
    validity = models.IntegerField()

class Advertisement(models.Model):
    ad_name = models.CharField(max_length=200,null=True,blank=True)
    ad_image = models.FileField(upload_to='Advertisements/')
    types = models.CharField(max_length=20,null=True,blank=True)

    @property
    def ImageURL(self):
        try:
            url = self.ad_image.url
        except:
            url = ''
        return url
    
    def delete(self, *args, **kwargs):
        self.ad_image.delete()
        super().delete(*args, **kwargs)


#homepage

class FeaturedShows(models.Model):
    show = models.ForeignKey('creator.Show', on_delete=models.CASCADE,null=True,blank=True)

class TopPodcasters(models.Model):
    creator = models.ForeignKey('creator.CreatorDeatails', on_delete=models.CASCADE,null=True,blank=True)

class TrendingShows(models.Model):
    show = models.ForeignKey('creator.Show', on_delete=models.CASCADE,null=True,blank=True)

class PopularShows(models.Model):
    show = models.ForeignKey('creator.Show', on_delete=models.CASCADE,null=True,blank=True)