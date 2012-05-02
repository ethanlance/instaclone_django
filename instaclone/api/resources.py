from django.contrib.auth.models import User
from django.utils import simplejson

from tastypie import fields
from tastypie.validation import Validation
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.serializers import Serializer

from instaclone.image.models import Image, Likes
from instaclone.userprofile.models import UserProfile, Following

from django.contrib.auth.models import User
from django.db import models
from tastypie.models import create_api_key
models.signals.post_save.connect(create_api_key, sender=User)

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
		authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()



class UserProfileResource(ModelResource):
	
	user = fields.OneToOneField(UserResource, 'user')

	class Meta:
		queryset = UserProfile.objects.all()
		resource_name = 'user_profile'
		fields = ['gender','fbid','username', 'follower_count', 'following_count', 'photo_count', 'id']
		filtering = {
			'fbid': ALL,
		}
		authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()



class ImageResource(ModelResource):
	
	user_profile = fields.ForeignKey(UserProfileResource, 'user_profile')
	
	class Meta:
		queryset = Image.objects.all()
		#filtering = {'user_profile':ALL_WITH_RELATIONS}
		allowed_methods = ['get']
		resource_name = 'image'
		authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()

	def get_object_list(self, request):
		profiles = []

		if 'user_profile_id' in request.GET:
			try:
				user_profile = UserProfile.objects.get(id=request.GET['user_profile_id'])
				profiles.append(user_profile)
			except UserProfile.DoesNotExist:
				return super(ImageResource,self).get_object_list(request)
		else:
			return super(ImageResource,self).get_object_list(request)


		
		if 'followers' in request.GET:
			following = Following.objects.all().filter(user_profile=user_profile)
			for u in following:
				profiles.append(u.user_profile2)

		return super(ImageResource, self).get_object_list(request).filter(user_profile__in=profiles)



class PopularImageResource(ModelResource):

	user_profile = fields.ForeignKey(UserProfileResource, 'user_profile')

	class Meta:
		queryset = Image.objects.filter(likes__gt=0).order_by("like_count")
		allowed_methods = ['get']
		resource_name = 'popular'
		authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()




class LikeResource(ModelResource):

	user_profile = fields.ForeignKey(UserProfileResource, 'user_profile')
	image = fields.ForeignKey(ImageResource, 'image')

	class Meta:
		queryset = Likes.objects.all()
		allowed_methods = ['post']
		authorization = Authorization()
		authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()

		
# Find images that yours that your followers liked.
class NewsResource(ModelResource):

	user_profile = fields.ForeignKey(UserProfileResource, 'user_profile')
	image = fields.ForeignKey(ImageResource, 'image')

	class Meta:
		queryset = Likes.objects.all()
		fields = ['id', 'datetime']
		authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()


	def get_object_list(self, request):
		
		profiles = []

		if 'user_profile_id' in request.GET:
			try:
				user_profile = UserProfile.objects.get(id=request.GET['user_profile_id'])				
			except UserProfile.DoesNotExist:
				return super(NewsResource,self).get_object_list(request)
		else:
			return super(NewsResource,self).get_object_list(request)
		
		following = Following.objects.all().filter(user_profile2=user_profile)
		for u in following:
			profiles.append(u.user_profile)

		return super(NewsResource, self).get_object_list(request).filter(user_profile__in=profiles)




#return the user this user follows
class FollowingResource(ModelResource):
	follower = fields.ForeignKey(UserProfileResource, 'user_profile')	
	following = fields.ForeignKey(UserProfileResource, 'user_profile2')	
	
	class Meta:
		queryset = Following.objects.all()	
		resource_name = 'following'
		filtering = {'follower':ALL_WITH_RELATIONS, 'following':ALL_WITH_RELATIONS}
		allowed_methods = ['post', 'get', 'delete']
		authorization = Authorization()
		authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
		






