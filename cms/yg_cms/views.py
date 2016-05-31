from django.shortcuts import render
from yg_cms.models import Column
from yg_cms.models import Article
from yg_cms.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone


def index(request):
    month = timezone.now().month
    articles = Article.objects.all().order_by('-pub_date')[:6]
    articles_recent = Article.objects.all().order_by('-pub_date')[:5]
    columns = Column.objects.all()
    if month == 5:
        months = [5, ]
        context = {'columns': columns, 'articles': articles, 'months': months, 'articles_recent': articles_recent}
    else:
        months = []
        for archive_month in range(month-4):
            months.append(archive_month+5)
        context = {'articles': articles, 'months': months, 'articles_recent': articles_recent}
    return render(request, 'yg_cms/index.html', context) #context_instance=RequestContext(request))


def column_detail(request, column_slug):
    month = timezone.now().month
    articles_recent = Article.objects.all().order_by('-pub_date')[:5]
    if column_slug == 'about':
        columns = Column.objects.all()
        context = {'columns': columns}
        return render(request,   'yg_cms/about.html', context)
    else:
        if month == 5:
            months = [5, ]
            columns = Column.objects.all()
            column = Column.objects.get(slug=column_slug)
            article_list = column.article_set.all()
            paginator = Paginator(article_list, 5) #实例化分页对象
            page = request.GET.get('page')
            try:
                article_list = paginator.page(page)
            except PageNotAnInteger:
                article_list = paginator.page(1)
            except EmptyPage:
                article_list = paginator.page(paginator.num_pages)
            context = {'column': column, 'columns': columns, 'article_list': article_list,
                       'articles_recent': articles_recent, 'months': months}
        else:
            months = []
            for archive_month in range(month-4):
                months.append(archive_month)
            columns = Column.objects.all()
            column = Column.objects.get(slug=column_slug)
            article_list = column.article_set.all()
            articles_recent = Article.objects.all().order_by('-pub_date')[:3]
            paginator = Paginator(article_list, 5)  # 实例化分页对象
            page = request.GET.get('page')
            try:
                article_list = paginator.page(page)
            except PageNotAnInteger:
                article_list = paginator.page(1)
            except EmptyPage:
                article_list = paginator.page(paginator.num_pages)
            context = {'column': column, 'columns': columns, 'article_list': article_list,
                       'articles_recent': articles_recent, 'months': months}
        return render(request, 'yg_cms/terms.html', context)


def article_detail(request, pk, article_slug):
    month = timezone.now().month
    columns = Column.objects.all()
    articles = Article.objects.get(pk=pk)
    pd = articles.pk
    if month == 5:
        months = [5, ]
        if Count.objects.filter(id=pd).exists():
            value = Count.objects.get(id=pd).count
            value += 1
            Count.objects.filter(id=pd).update(count=value)
        else:
            Count.objects.create(id=pd, count=1)
            count = Count.objects.get(id=pd)
            value = count.count
        context = {'months': months, 'articles': articles, 'columns': columns, 'value': value, 'pd': pd}
    else:
        months = []
        for archive_month in range(month - 4):
            months.append(archive_month + 5)
        if Count.objects.filter(id=pd).exists():
            value = Count.objects.get(id=pd).count
            value += 1
            Count.objects.filter(id=pd).update(count=value)
        else:
            Count.objects.create(id=pd, count=1)
            count = Count.objects.get(id=pd)
            value = count.count
        context = {'months': months, 'articles': articles, 'columns': columns, 'value': value, 'pd': pd}
    return render(request, 'yg_cms/single.html', context)


def archive(request, archive_slug):
    columns = Column.objects.all()
    archives = Article.objects.filter(pub_date__month=archive_slug)
    paginator = Paginator(archives, 5)
    page = request.GET.get('page')
    try:
        archives = paginator.page(page)
    except PageNotAnInteger:
        archives = paginator.page(1)
    except EmptyPage:
        archives = paginator.page(paginator.num_pages)

    context = {'archives': archives, 'columns': columns}
    return render(request, 'yg_cms/archive.html', context)
