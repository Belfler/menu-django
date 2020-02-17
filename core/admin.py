from django.contrib import admin

from core.models import *


class MenuPointInline(admin.TabularInline):
    model = MenuPoint


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    fields = ['title']
    inlines = [MenuPointInline]


@admin.register(MenuPoint)
class MenuPointAdmin(admin.ModelAdmin):
    list_display = ['title', 'menu', 'depth', 'parent', 'url_name']
    ordering = ['depth']
