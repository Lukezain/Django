# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse


@python_2_unicode_compatible
class Column(models.Model):
    name = models.CharField('目录名称', max_length=256)
    slug = models.CharField('目录网址', max_length=256, db_index=True)
    intro = models.TextField('目录简介', default='')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('column', args=(self.slug,))

    class Meta:
        verbose_name = '目录'
        verbose_name_plural = '目录'
        # ordering = ['name']  # 按照哪个栏目排序


@python_2_unicode_compatible
class Article(models.Model):
    column = models.ManyToManyField(Column, verbose_name='归属目录')

    title = models.CharField(verbose_name='标题', max_length=256)
    slug = models.CharField('网址', max_length=256, unique=True)

    author = models.ForeignKey('auth.User', blank=True, null=True, verbose_name='作者')
    content = models.TextField('内容')

    published = models.BooleanField('正式发布', default=True)
    pub_date = models.DateTimeField('发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', args=(self.pk, self.slug))

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'


class Count(models.Model):
    id = models.IntegerField(verbose_name='ID', primary_key=True)
    count = models.IntegerField(verbose_name="计数")

    def __str__(self):
        return self.id
