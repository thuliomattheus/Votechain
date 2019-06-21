from django.contrib import admin
from clientProject.clientApp import models

admin.site.register(models.User)
admin.site.register(models.Vote)
admin.site.register(models.Seeder)
