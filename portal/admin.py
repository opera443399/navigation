# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.contrib import admin
from .models import Level1BizGroup, Level2WorkGroup, Level3App, Level4AppCategory, Level5AppLink

# Register your models here.


class Level2WorkGroupinline(admin.TabularInline):
    model = Level2WorkGroup
    extra = 0


@admin.register(Level1BizGroup)
class Level1BizGroupAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_select_related = ()
    inlines = (Level2WorkGroupinline,)
    list_display = ('bg_id', 'bg_name')
    list_filter = ['bg_name']
    search_fields = ['bg_id', 'bg_name']


class Level3Appinline(admin.TabularInline):
    model = Level3App
    extra = 0


@admin.register(Level2WorkGroup)
class Level2WorkGroupAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_select_related = ()
    inlines = (Level3Appinline,)
    list_display = ('wg_id', 'wg_name', 'bg')
    list_filter = ['bg']
    search_fields = ['wg_id', 'wg_name', 'bg__bg_name']


class Level4AppCategoryinline(admin.TabularInline):
    model = Level4AppCategory
    extra = 0


@admin.register(Level3App)
class Level3AppAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_select_related = ()
    inlines = (Level4AppCategoryinline,)
    fieldsets = [
        (None, {'fields': ['app_id', 'app_name', 'app_ename', 'wg']}),
        (_('Visibility'), {'fields': ['is_enabled']}),
    ]
    list_display = ('app_id', 'app_name', 'app_ename', 'wg', 'is_enabled')
    list_filter = ['wg', 'is_enabled']
    search_fields = ['app_id', 'app_name', 'app_ename', 'wg__wg_name', 'is_enabled']


class Level5AppLinkInline(admin.TabularInline):
    model = Level5AppLink
    extra = 0


@admin.register(Level4AppCategory)
class Level4AppCategoryAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_select_related = ()
    inlines = (Level5AppLinkInline,)
    list_display = ('id', 'cat_name', 'cat_rank', 'app')
    list_filter = ['cat_rank', 'app']
    search_fields = ['id', 'cat_name', 'cat_rank', 'app__app_name']


@admin.register(Level5AppLink)
class Level5AppLinkAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_select_related = ()
    fieldsets = [
        (None, {'fields': ['link_name', 'link_href', 'link_img', 'cat']}),
        (_('optional'), {'fields': ['link_img_upload'], 'classes': ['collapse']}),
    ]
    list_display = ('id', 'link_name', 'link_href', 'link_img', 'link_img_upload', 'cat')
    list_filter = ['cat']
    search_fields = ['id', 'link_name', 'link_href', 'link_img', 'link_img_upload', 'cat__cat_name']
