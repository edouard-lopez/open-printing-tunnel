from django.contrib import admin

from api import models

admin.site.register(models.Company)
admin.site.register(models.RemoteNode)
admin.site.register(models.OptUser)
