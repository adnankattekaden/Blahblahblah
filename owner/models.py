from django.db import models
        
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

    