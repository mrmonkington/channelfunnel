from django.core.management.base import BaseCommand
import os
from django.conf import settings
from pprint import pprint
import logging
from content.models import Source, Article

import feedparser
from datetime import datetime

from ngram import NGram

#class NGramArticle( NGram ):
#    def iconv( item ):
#        return unicode( item )

import re

class Command( BaseCommand ):

    def normalise( self, title ):
        title = re.sub( "News:\s*", "", title )
        title = re.sub( "\s{2,}", " ", title )
        return title.strip()

    def handle( self, *args, **options ):
        if "simonly" in args:
            new_count = 200
        else:
            new_count = 0
            for source in Source.objects.filter( scraper = 'feedparser', status__in = ( 'silent', 'live' ) ):
                l = feedparser.parse( source.scraper_config )
                ok = True
                if l[ "bozo" ] == 1:
                   if not isinstance( l[ "bozo_exception" ], feedparser.ThingsNobodyCaresAboutButMe ):
                       ok = False
                if ok:
                    for article in l[ "entries" ]:
                        print "Reading feed entry %s: '%s'" % ( article[ "id" ], article[ "title" ] )
                        a, created = Article.objects.get_or_create(
                            source = source,
                            # Wordpress RSS IDs are unique internet-wide, and are immutable (unlike URLs)
                            source_reference = article[ "id" ],
                            defaults = {
                                'date_created' : datetime.now(),
                                'source_url' : article[ "link" ],
                                'title' : self.normalise( article[ "title" ] ),
                                'num_comments' : article.get( "slash_comments", 0 ),
                                'summary' : article[ "summary" ],
                                'author' : article.get( "author", "" ),
                                'date_published' : datetime(*(article[ "date_parsed" ][:6])),
                                'status' : "live"
                            }
                        )
                        if created:
                            print "Creating new article."
                        else:
                            print "Updating article."
                        new_count += 1
                        if article.has_key( "content" ):
                            # TODO test for multiple content blocks and pick most appropriate
                            a.body = article[ "content" ][0][ "value" ]
                        a.tags.clear()
                        for tag in article.get( "tags", () ):
                            a.tags.add( tag[ "term" ] )
                        a.save()

                else:
                    logging.error( "Could not read feed for file '%s': %s" % ( source.scraper_config, l[ "bozo_exception" ] ) ) 
                    logging.error( "Skipping '%s': %s" % ( source.scraper_config, l[ "bozo_exception" ] ) ) 
                    break

        #calculate similarities
        #create a similarity corpus of last 200 docs

        def enrich( obj ):
            s = unicode( obj )
            s = re.sub( r"\b(the|of|in|a)\b", "", s, re.IGNORECASE )
            return s
        n = NGram( warp=2.5, iconv=enrich )
        articles = Article.objects.filter( status = "live" ).order_by( "date_published" )[:(new_count*4)]
        for article in articles:
        #articles = Article.objects.filter( status = "live", is_duplicate = False ).order_by( "-date_published" )[:new_count]
        #for article in articles:
            print( u"similarity for %s" % ( article.title, ) )
            sim = filter( lambda a: a[1] > 0.4, n.search( article.title ) )
            if len( sim ) > 0:
                nearest = sim[0][0]
                if nearest.is_duplicate:
                    nearest = nearest.duplicate_of
                article.is_duplicate = True
                article.duplicate_of = nearest
                print u" is duplicate of %s" % ( nearest.title, )
                article.save()
            n.add( article )


