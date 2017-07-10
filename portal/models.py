# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.db import models

from .apps import CHOICES_ICONS

# Create your models here.


@python_2_unicode_compatible
class Level1BizGroup(models.Model):
    bg_id = models.IntegerField(_('id'), unique=True, default=1)
    bg_name = models.CharField(_('name'), max_length=50, unique=True, default='DEFAULT')
    bg_rank = models.IntegerField(_('rank'), default=0)

    def __str__(self):
        return self.bg_name

    class Meta:
        verbose_name = _('biz group')
        verbose_name_plural = _('biz group')


@python_2_unicode_compatible
class Level2WorkGroup(models.Model):
    wg_id = models.IntegerField(_('id'), unique=True, default=1)
    wg_name = models.CharField(_('name'), max_length=50, unique=True, default='DEFAULT')
    wg_rank = models.IntegerField(_('rank'), default=0)
    added_to_navbar = models.BooleanField(_('added to navbar?'), default=False)
    bg = models.ForeignKey(Level1BizGroup, default='1', on_delete=models.CASCADE, verbose_name=_('biz group'))

    def __str__(self):
        return self.wg_name

    class Meta:
        verbose_name = _('work group')
        verbose_name_plural = _('work group')


@python_2_unicode_compatible
class Level3App(models.Model):
    app_id = models.IntegerField(_('id'), unique=True, default=1)
    app_name = models.CharField(_('name'), max_length=50, unique=True, default='DEFAULT')
    app_ename = models.CharField(_('en name'), max_length=50, unique=True, default='DEFAULT')
    is_enabled = models.BooleanField(_('is enabled?'), default=False)
    app_rank = models.IntegerField(_('rank'), default=0)
    wg = models.ForeignKey(Level2WorkGroup, default='1', on_delete=models.CASCADE, verbose_name=_('work group'))

    def __str__(self):
        return self.app_name

    class Meta:
        verbose_name = _('app')
        verbose_name_plural = _('app')


@python_2_unicode_compatible
class Level4AppCategory(models.Model):
    cat_name = models.CharField(_('name'), max_length=50, unique=True, default='DEFAULT')
    cat_rank = models.IntegerField(_('rank'), default=0)
    app = models.ForeignKey(Level3App, default='1', on_delete=models.CASCADE, verbose_name=_('app'))

    def __str__(self):
        return self.cat_name

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('category')


@python_2_unicode_compatible
class Level5AppLink(models.Model):
    link_name = models.CharField(_('name'), max_length=50, unique=True, default='DEFAULT')
    link_href = models.CharField(_('href'), max_length=500, default='#')
    link_img = models.CharField(_('icon'), max_length=50, choices=CHOICES_ICONS, default='icons/default.svg')
    link_img_upload = models.ImageField(_('custom icon'), upload_to='icons', default='', blank=True)
    cat = models.ForeignKey(Level4AppCategory, default='1', on_delete=models.CASCADE, verbose_name=_('category'))

    def __str__(self):
        return self.link_name

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('link')

