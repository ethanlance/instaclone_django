from django.conf.urls.defaults import patterns, include, url
from instaclone.image.models import Image

from tastypie.api import Api
from instaclone.api.resources import ImageResource, UserProfileResource, UserResource, PopularImageResource, LikeResource, NewsResource, FollowingResource

image_resource = ImageResource()

v1_api = Api(api_name='v1')
v1_api.register(UserProfileResource())
v1_api.register(UserResource())
v1_api.register(ImageResource())
v1_api.register(PopularImageResource())
v1_api.register(LikeResource())
v1_api.register(NewsResource())
v1_api.register(FollowingResource())

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'image.views.image_feed_view'),
    # url(r'^instaclone/', include('instaclone.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    
    url(r'^upload/', 'image.views.upload_file'),
    url(r'^login_or_signup', 'image.views.login_or_signup'),
    
    # (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    # (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    # (r'^password_change/$', 'django.contrib.auth.views.password_change', {'post_change_redirect':'/'}),
    
     (r'^api/', include(v1_api.urls)),
)
