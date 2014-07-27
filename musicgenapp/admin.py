from django.contrib import admin
from musicgenapp.models import *

# Register your models here.

admin.site.register(MusicGenUser)
admin.site.register(Song)
admin.site.register(SongWrapper)
admin.site.register(Rating)