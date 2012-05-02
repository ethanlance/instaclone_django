from django.db import models
from django import forms
from instaclone.image.s3imagefield import S3EnabledImageField
from instaclone.userprofile.models import UserProfile
import datetime
 
class Image(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='images')
    image = S3EnabledImageField(upload_to='/static/images')
    datetime = models.DateTimeField(blank=True, default=datetime.datetime.now)
    like_count = models.SmallIntegerField(blank=True, null=True, default=0)
    comment_count = models.SmallIntegerField(blank=True, null=True, default=0)    
    
    
class Likes(models.Model):
    image = models.ForeignKey(Image, related_name='likes')
    user_profile = models.ForeignKey(UserProfile, related_name='likes')
    datetime = models.DateTimeField(blank=True, default=datetime.datetime.now)

    def save(self, **kwargs):

        #Tasty Pie, cuz im dumb...
        try:
            like = Likes.objects.get(image=self.image, user_profile=self.user_profile)
            return
        except Likes.DoesNotExist:
            pass
        
        super(Likes, self).save(**kwargs)
        
        self.image.like_count = self.image.like_count + 1
        self.image.save()    

        self.user_profile.photo_count = self.user_profile.photo_count + 1
        self.user_profile.save()
        
    class Meta:
        unique_together = (('user_profile','image' ),)

    
class Comments(models.Model):
    image = models.ForeignKey(Image, related_name='comments')
    user_profile = models.ForeignKey(UserProfile, related_name='comments')
    datetime = models.DateTimeField(blank=True, default=datetime.datetime.now)
    comment = models.TextField(blank=True)
    