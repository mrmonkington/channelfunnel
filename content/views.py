from models import *
from django.shortcuts import render
from django.core import serializers
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from taggit.models import Tag
import json
import re

WARP = 2.5

from ngram import NGram
import datetime
import time

import unicodedata
import sys

def longest_common_substring(s1, s2):
    m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]

tbl = dict.fromkeys(
    i for i in xrange(sys.maxunicode)
    if unicodedata.category(unichr(i)).startswith('P')
)

def common_terms( ss ):
    ts = None
    ordering = None
    for s in ss:
        l = s.lower().translate(tbl).split()
        st = set(l)
        if ts != None:
            ordering = l
            ts = ts & st
        else:
            ts = st

    print ts
    print ordering
    op = sorted(list(ts), key = lambda k : ordering.index(k))
    if len(op) == 0:
        return "<no topic - possibly a duff group>"
    return " ".join( op )

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

def enrich( obj ):
    s = unicode( obj )
    # simple stop words
    s = re.sub( r"\b(the|of|in|a)\b", "", s, re.IGNORECASE )
    # type prefixes
    s = re.sub( r"^(trailer|review|report|screenshots|video|watch):\s*", "", s, re.IGNORECASE )
    s = re.sub( r"\[update\]\s*$", "", s, re.IGNORECASE )
    return s

def simtitle( request ):
    """calculate similarity based on title and naive threshold"""
    n = NGram( warp=WARP, iconv=enrich, key=lambda x: x.title )
    articles = Article.objects.filter( status = "live" ).order_by( "date_published" )[:1000]
    results = []
    for article in articles:
        article.is_duplicate = False
        article.duplicate_of = None
        article.save()
        sim = filter( lambda a: a[1] >= 0.4, n.search( article.title ) )
        for match in sim:
            nearest = match[0]
            if nearest.is_duplicate:
                nearest = nearest.duplicate_of
                if NGram.compare( article.title, nearest.title ) < 0.7:
                    results.append( article )
                    break
            article.is_duplicate = True
            article.duplicate_of = nearest
            article.save()
            break
        else:
            results.append( article )
        n.add( article )
    return render( request, "dump.html", dictionary = { "article_list": results, } )

def clustertitle( request ):
    """cluster based on title and ngram sim"""

    from cluster import HierarchicalClustering

    def sim( a, b ):
        return 1 - NGram.compare( a.title, b.title, warp=WARP, iconv=enrich )

    articles = Article.objects.filter( status = "live", date_published__gte = datetime.datetime.now() - datetime.timedelta(1) ).order_by( "date_published" )[:1000]
    cl = HierarchicalClustering(articles, sim)
    # 0.7 chosen pretty much through trial and error :)
    res = cl.getlevel(0.7)
    #import pprint
    #pprint.pprint( cl.topo() )

    clusters = []
    for cluster in res:
        if len(cluster) > 1:
            node = {
                    'type': 'cluster',
                    #'topic': longest_common_substring(cluster[0].title, cluster[1].title),
                    'topic': common_terms( [a.title for a in cluster] ),
                    'articles': cluster
                    }
        else:
            node = {
                    'type': 'article',
                    'article': cluster[0]
            }
        clusters.append(node)

    return render( request, "clusters.html", dictionary = { "clusters": clusters, } )

def simsummary( request ):
    articles = Article.objects.filter( status = "live", is_duplicate = False ).order_by( "title" )
    return render( request, "dump.html", dictionary = { "article_list": articles, } )

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
