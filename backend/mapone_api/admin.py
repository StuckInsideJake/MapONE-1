from django.contrib import admin

from .models import User, Entry, Archive

admin.site.register(User)
admin.site.register(Entry)
admin.site.register(Archive)
