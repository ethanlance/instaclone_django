instaclone_django
=================


Also Need:
---------
Amazon S3 account.  If you want to upload images get an account and fill this section of settings.py out:

<code>
USE_AMAZON_S3 = True
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
AWS_TEMP_UPLOAD_BUCKET = 'instaclonebucket'
AWS_TEMP_UPLOAD_DIRECTORY = 'uploads/'
</code>



Setup
-----

Set up a virtualenv 

<code>virtualenv venv --distribute</code>

<code>source venv/bin/activate</code>

Now install all the requirements (like Django and Tastypie):

<code>cd instaclone_django</code>

<code>pip install -r requirements.txt</code>

<code>cd instaclone_django/instaclone</code>

Create our sqlite3 database:

<code>python manage.py syncdb</code>
Say "NO" to creating an admin user. Or you'll get an error later on because tastypie will not have created an api_key for this user.  I let the iOS app create the 1st user.

Start the server. I'm using a Mac and Bonjour to make this work:

<code>python manage.py runserver 0.0.0.0:8000</code>
For mac (dunno about windows, sorry) go System Preferences > Sharing.  Under Computer Name click "Edit".  Copy localhost name and use it in the constants.h file where we define: #define BASE_URL @"http://lancebook.local:8000/" 

