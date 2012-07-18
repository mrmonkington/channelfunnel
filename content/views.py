from models import *
from django.shortcuts import render
from django.core import serializers
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from taggit.models import Tag
import json
import datetime
import time

def click( request, article_id ):
    article = get_object_or_404( Article, pk = article_id, status = "live" )
    return HttpResponseRedirect( Article.source_url )

def home( request ):
    offset = ( int( request.GET.get( "page", 1 )) - 1 ) * settings.PAGE_SIZE
    articles = Article.objects.filter( status = "live", is_duplicate = False ).order_by( "-date_published" )[offset:offset+settings.PAGE_SIZE]
    if not request.is_ajax():
        return render( request, "full_list.html", dictionary = { "article_list": articles, } )
    else:
        return render( request, "ajax_list.html", dictionary = { "article_list": articles, } )

def new( request, since ):
    since = int( since );
    if since > 0:
        since = datetime.datetime.fromtimestamp( since );
        # limit to prevent DOSing
        articles = Article.objects.filter( status = "live", is_duplicate = False, date_published__gt = since ).order_by( "-date_published" )[:100]
        if settings.DEBUG or request.is_ajax():
            return render( request, "ajax_list.html", dictionary = { "article_list": articles, } )
    return HttpResponse("")
    
def filter_source( request, source ):
    offset = ( int( request.GET.get( "page", 1 )) - 1 ) * settings.PAGE_SIZE
    source_obj = get_object_or_404( Source, code = source )
    articles = Article.objects.filter( source = source_obj, status = "live", is_duplicate = False ).order_by( "-date_published" )[offset:offset+settings.PAGE_SIZE]
    filter_title = "Showing articles from %s" % ( source_obj.title )
    if not request.is_ajax():
        return render( request, "full_list.html", dictionary = { "filter_title": filter_title, "article_list": articles, } )
    else:
        return render( request, "ajax_list.html", dictionary = { "article_list": articles, } )

def filter_tag( request, tag ):
    offset = ( int( request.GET.get( "page", 1 )) - 1 ) * settings.PAGE_SIZE
    tag_obj = get_object_or_404( Tag, slug = tag )
    articles = Article.objects.filter( tags__slug__in = [ tag, ], status = "live", is_duplicate = False ).order_by( "-date_published" )[offset:offset+settings.PAGE_SIZE]
    filter_title = "Showing articles tagged %s" % tag_obj.name
    if not request.is_ajax():
        return render( request, "full_list.html", dictionary = { "filter_title": filter_title, "article_list": articles, } )
    else:
        return render( request, "ajax_list.html", dictionary = { "article_list": articles, } )
    
def search_autocomplete( request ):
    term = request.GET.get( "term", "" )
    tags = Tag.objects.filter( name__contains = term )
    tags_resp = json.dumps(
        [
            { 'value': tag.name, 'url': reverse( 'filter_tag', args = ( tag.slug, ) ) }
            for tag in tags
        ]
    )
    return HttpResponse( tags_resp )

def search( request ):
    offset = ( int( request.GET.get( "page", 1 )) - 1 ) * settings.PAGE_SIZE
    term = request.GET.get( "term", "" )
    articles = Article.objects.filter( tags__name__contains = term, status = "live", is_duplicate = False ).order_by( "-date_published" )[offset:offset+settings.PAGE_SIZE]
    filter_title = "Showing articles tagged %s" % term
    if not request.is_ajax():
        return render( request, "full_list.html", dictionary = { "term": term, "filter_title": filter_title, "article_list": articles, } )
    else:
        return render( request, "ajax_list.html", dictionary = { "article_list": articles, } )
