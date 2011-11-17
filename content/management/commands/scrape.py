from django.core.management.base import BaseCommand
import os
from django.conf import settings
from pprint import pprint
import logging
from content.models import Source, Article

import feedparser

class Command( BaseCommand ):

    def handle( self, *args, **options ):
        for source in Source.objects.filter( scraper = 'feedparser', status__in = ( 'silent', 'live' ) ):
            l = feedparser.parse( source.scraper_config )
            if l[ "bozo" ] == 0 :
                for article in l[ "entries" ]:
                    
                return
            else:
                logging.error( "Could not read feed for file '%s': %s" % ( args[0], l[ "bozo_exception" ] ) ) 
                logging.error( "Skipping '%s': %s" % ( args[0], l[ "bozo_exception" ] ) ) 
                break

