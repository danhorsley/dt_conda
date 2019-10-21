# django nightmares
conda env list if env already created)
conda create --name whatever_env
conda activate whatever_env

Clone your repo
(If you cloned the Hello-Django repo, delete the file requirements.txt!)
Go to your repo root directory

conda install -c anaconda django

django-admin startproject my_project_name .   <-----do not forget . at the end
django-admin startapp my_app name
python manage.py runserver (should show rocket ship on internet link)

make your own class in your app file using models.Model

class Note(models.Model):
    """placeholder"""
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    new_field = 'nf'

conda install -c conda-forge python-decouple

from decouple import config into your settings.py

Add the key your .env file (creating it if you have to):

SECRET_KEY='...whatever it was in the settings file...'

SECRET_KEY = config('SECRET_KEY')

same for DEBUG

DEBUG = config('DEBUG', cast=bool)

verify that .env is in .gitignore and commit.

if you need new key....
import random
''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)]) # All one line!


** make your environment.yml
conda env export > environment.yml

** admin functions

run python manage.py runserver
if you go on http://127.0.0.1:8000/admin/ you will see login page
make a super user with 
python manage.py createsuperuser

runserver to check it
and it will take you to administration page

now you to your app file
in teh admin.py do this

from .models import Note  (or whatever your class was called)
admin.site.register(Note)

for extra ntoes etc.
admin.site.register(PersonalNote) 

now looking at SQL
python manage.py dbshell
.tables will display a list of tables

pragma table_info(notes_note); 			displays cols for specified table

SELECT * FROM notes_note;  		to show tabe ontents all - don't forget semi colon

https://github.com/LambdaSchool/Intro-Django/blob/master/guides/day3.md

https://github.com/LambdaSchool/Intro-Django/blob/master/guides/day4.md

https://www.youtube.com/watch?v=0qsOwWTo2wc      ** this graphql

Project Set Up
Note: the instructions below assume you're on your master branch in git.

The steps to deploy (at a high level) are:

Sign up for Heroku

Install the Heroku CLI

From your terminal, heroku login

Get to your project/repo directory

Install new dependencies. (If using virtualenv, use pip install as you have been, or migrate to pipenv.)

pipenv install gunicorn - the webserver for Heroku to use (rather than the one built-in to Django)
pipenv install psycopg2-binary - PostgreSQL client binaries
pipenv install dj-database-url - enables parameterizing the database connection (so Heroku uses PostgreSQL but local is still SQLite)
pipenv install whitenoise - optimizes deployment of static files (you may not have any, but it's good to add this now)
If using virtualenv, you need to create a requirements.txt file in your project root directory with the command: pip freeze > requirements.txt
Prepare your project

Copy the dotenv file in this repository to .env in your repository (this should not be checked in)
ALLOWED_HOSTS and DATABASE_URL are probably already correct for your local environment, but read/understand them
Use the example code (you can just run it in a python repl) to generate a new secret key and change SECRET_KEY
djorg/settings.py will need new imports (from decouple import config and import dj_database_url)
You can use config to load the environment variables you set above, e.g. SECRET_KEY = config('SECRET_KEY') (ALLOWED_HOSTS will be a little trickier, but that's why this is a sprint challenge!)
For the database, you want to both load the DATABASE_URL and pass it to dj_database_url.config (see documentation)
Make a Procfile (example) to tell Heroku what to run to start your app. (Hint: the name of your Django project is probably "djorg", not "gettingstarted".)
Configure whitenoise (add a few configuration lines to your settings.py file per the documentation)
Add static settings to your settings.py:
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
heroku create your-app - makes the project and adds Heroku as a remote to your git repository so you can push to it to deploy

heroku addons:create heroku-postgresql:hobby-dev - makes a PostgreSQL database associated with the project (and sets the DATABASE_URL Heroku config var, equivalent to a local environment variable)

Set the other Heroku config vars, e.g. ALLOWED_HOSTS=.herokuapp.com, DEBUG=False, and SECRET_KEY=somenewsecret - see the documentation, you can set either via the Heroku CLI or by logging in to the Heroku Dashboard in your browser

Deploy! First, make sure you're all committed. Then git push heroku master

Once you've got it deployed, you'll probably need to run migrations on Heroku (since it's using a different database then local). You can do this with heroku run python manage.py migrate, and in general heroku run python manage.py is the way to do all the helpful Django things, just "in production." For example, heroku run python manage.py createsuperuser is a good thing to do, and you can even administer/explore the app/data with heroku run python manage.py shell and heroku run python manage.py dbshell.

Troubleshooting
Getting Started on Heroku with Python - official tutorial, has a full working example app if you want to step through with that before you try with Djorg
Lambda School Python/Django resources
You may also find the heroku logs command useful to diagnose errors, as Heroku error messages are usually not that descriptive.

Bash prompt doesn't echo and RETURN doesn't go to the next line
Note for bash users: if you ever get in a place where your terminal isn't printing out newlines properly and is not echoing your keypresses, hit CTRL-C then blindly type in the following command and hit RETURN:

stty sane
Whitenoise incompatible with Version 4.0
If you get errors along these lines, make sure your STATICFILES_STORAGE is set to Compressed and not to Gzip.

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
Example working MIDDLEWARE config:

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
Modules installed locally, but not on Heroku
Make sure the module is in your Pipfile. If it's not, you probably installed it with pip instead of pipenv.

If the module appears in pip list:

pip uninstall modulename
pipenv install modulename
Then try to redeploy.

Improperly configured databases
Error:

raise ImproperlyConfigured("settings.DATABASES is improperly configured. "
django.core.exceptions.ImproperlyConfigured: settings.DATABASES is improperly configured. Please supply the ENGINE value. Check settings documentation for more details.
Try this in your settings.py:

DATABASES = {}

DATABASES['default'] = dj_database_url.config(default=config('DATABASE_URL'), conn_max_age=600)
Another option:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
Minimum Viable Product
Your finished project must include all of the following requirements:

A link to your Djorg project repo
A link to your live site, if you were able to deploy
Completed summary of your deployment process in DeploymentExperiences.md
In your solution, it is essential that you follow best practices and produce clean and professional results. Schedule time to review, refine, and assess your work and perform basic professional polishing including spell-checking and grammar-checking on your work. It is better to submit a challenge that meets MVP than one that attempts too much and does not.

Stretch Problems
After finishing your required elements, you can push your work further. These goals may or may not be things you have learned in this module but they build on the material you just studied. Time allowing, stretch your limits and see if you can deliver on the following optional goals:

Teach others what you have learned about Django development. Write a blog post or short article. Consider easy-to-read formats like a how-to guide or top 5 list. Do NOT just publish your answers to the Self-Study/Essay Questions section. You may use this content as a starting point, but it must be expanded upon in a significant, transformative way. Or focus on one or two specific pieces of Django you explored this week and describe how to use them or why they are useful with a high level of technical detail.

Publish your writing on your own personal blog or website or submit it to a larger publication like Medium or Hackernoon. Show that you completed this stretch goal by submitting the following in a seperate folder in your repo name stretch_write:

DjangoExperiences.md file with the final text.
A link to the published piece OR screenshot showing your submitted it to be published on another site.
Explore how Heroku logging works. Try generating, retrieving, and filtering log messages from your app. Show that you completed this stretch goal by submitting the following in a seperate folder in your repo named stretch_log:

A short paragraph describing the steps you took to implement logs, saved in LoggingExperiences.md. Include some of the statements you wrote to generate logs from within your application.
A screenshot that show logs being viewed from the terminal.
A second screenshot that shows logs being fetched with filtering arguments. Try fetching with filters at least two times, using different filters each time.




