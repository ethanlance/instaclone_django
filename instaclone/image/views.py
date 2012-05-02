from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseServerError
from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from tastypie.models import ApiKey

from instaclone.image.models import Image, Likes
from instaclone.userprofile.models import UserProfile
 

import pprint

@csrf_exempt
def login_or_signup(request):

    user = False;
    username = False;
    email = "tmp@app.com"
    password = "tmppass"

    displayname = request.POST['name']
    fbid = request.POST['fbid']
    
    #Do we already have this user?
    
    if "email" in request.POST:
        email = request.POST['email']
        username = email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass

    if fbid and not user:
        username = fbid
        try:
            user_profile = UserProfile.objects.get(fbid=fbid)
            user = user_profile.user
        except UserProfile.DoesNotExist:
            pass

    if not user:
        user = User.objects.create_user(fbid, email, password)

    #tastypie api_key
    api = ApiKey.objects.get(user=user)

    #Update user_profile:
    user_profile = user.get_profile()
    user_profile.username = displayname
    user_profile.fbid = fbid
    user_profile.save()
 
    dic = list()
    dic.append({
        'username':user_profile.username, 
        'user_profile_id':user_profile.id,
        'fbid':fbid,
        'api_username':user.username,
        'api_key':api.key
    })
    return HttpResponse(simplejson.dumps(dic, cls=DjangoJSONEncoder), mimetype='application/json') 

@csrf_exempt
def upload_file(request):
    
    
    fbid = request.POST['fbid']
    
    user_profile = UserProfile.objects.get(fbid=fbid)
    
    for filename, file in request.FILES.iteritems():    
        d = Image()
        d.image = file
        d.user_profile = user_profile
        d.save()
        pprint.pprint(d)
    
    return HttpResponse('OK')
    
