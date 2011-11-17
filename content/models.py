from django.db import models

from taggit.managers import TaggableManager

# Create your models here.

class Source( models.Model ):
    title = models.CharField( max_length = 200 )
    description = models.TextField( blank = True )
    scraper = models.CharField( max_length = 50, choices = (
        ( 'native', 'Original research' ),
        ( 'feedparser', 'Imported from external feed' ),
    ) )
    scraper_config = models.TextField()
    code = models.CharField( max_length = 50, blank = False )
    status = models.CharField( max_length = 10, choices = (
        ( "deleted", "Deleted - all old and new articles will be hidden, feed will not run." ),
        ( "silent", "Silent running - feed will continue to be read, but old and new content will not show on live site", ),
        ( "frozen", "Frozen - old content will show but feed will not longer be read" ),
        ( "live", "Live - what is says on the tin" ),
    ) )

class ScrapeLog( models.Model ):

class Article( models.Model ):
    source = models.ForeignKey( Source, blank = False )

    status = models.CharField( max_length = 10, choices = (
        ( "deleted", "Deleted" ),
        ( "offline", "Offline", ),
        ( "pending", "Pending" ),
        ( "live", "Live" ),
    ) )
    is_duplicate = models.BooleanField( default = False, null = False )
    duplicate_of = models.ForeignKey( "Article", blank = True )
    date_created = models.DateTimeField( blank = False )

    # unique ID as defined by source - for updates
    source_reference = models.CharField( max_length = 50, unique = True, blank = False )
    source_url = models.CharField( max_length = 250, blank = True )
    title = models.TextField( blank = False )
    summary = models.TextField( blank = True )
    body = models.TextField( blank = True )
    image = models.TextField( blank = True )
    author = models.TextField( blank = True )
    date_published = models.DateTimeField( blank = True )
    tags = TaggableManager
