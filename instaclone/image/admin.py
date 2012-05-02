from django.contrib import admin
from instaclone.image.models import Image

class ImageAdmin(admin.ModelAdmin):
	list_display = ["image", "user_profile", 'datetime']
	list_editable = ['user_profile']
	pass
    
admin.site.register(Image, ImageAdmin)