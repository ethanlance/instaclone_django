from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from tastypie.models import create_api_key


GENDER_CHOICE_MALE = 1
GENDER_CHOICE_FEMALE = 2
GENDER_CHOICE_OTHER = 3

GENDER_CHOICES = (
    (GENDER_CHOICE_MALE, 'Male'),
    (GENDER_CHOICE_FEMALE, 'Female'),
    (GENDER_CHOICE_OTHER, 'Other'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, null=True)
    fbid = models.TextField(null=True)
    username = models.TextField(null=True)

    follower_count = models.SmallIntegerField(blank=True, null=True, default=0)    
    following_count = models.SmallIntegerField(blank=True, null=True, default=0)    
    photo_count = models.SmallIntegerField(blank=True, null=True, default=0)
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

	
post_save.connect(create_api_key, sender=User)
post_save.connect(create_user_profile, sender=User)    


class Following(models.Model):
	user_profile = models.ForeignKey(UserProfile, related_name='follower')
	user_profile2 = models.ForeignKey(UserProfile, related_name='followed')

	def save(self, **kwargs):

		self.user_profile.follower_count = self.user_profile.follower_count + 1
		self.user_profile.save()

		self.user_profile2.following_count = self.user_profile2.following_count + 1
		self.user_profile2.save()

		super(Following, self).save(**kwargs)

	def delete(self, **kwargs):

		if self.user_profile.follower_count > 0:
			self.user_profile.follower_count = self.user_profile.follower_count - 1
			self.user_profile.save()

		if self.user_profile2.follower_count > 0:
			self.user_profile2.following_count = self.user_profile2.following_count - 1
			self.user_profile2.save()

		super(Following, self).delete(**kwargs)


	class Meta:
		unique_together = (('user_profile','user_profile2' ),)



