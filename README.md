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




