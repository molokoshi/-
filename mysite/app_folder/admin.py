"""Admin for app"""
from django.contrib import admin
from .models import DetailInfo, FacebookSearch, BaseInfo

admin.site.register(DetailInfo)
admin.site.register(FacebookSearch)
admin.site.register(BaseInfo)
