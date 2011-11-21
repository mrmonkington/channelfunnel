from models import *
from django.shortcuts import render
from django.core import serializers
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import get_object_or_404

from taggit.models import Tag

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
    
