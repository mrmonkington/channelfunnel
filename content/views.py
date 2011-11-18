from models import *
from django.shortcuts import render
from django.core import serializers
from django.conf import settings

def home( request ):
    #offset = request.GET.get( "offset", 0 )
    offset = ( int( request.GET.get( "page", 1 )) - 1 ) * settings.PAGE_SIZE
    articles = Article.objects.filter( status = "live", is_duplicate = False ).order_by( "-date_published" )[offset:offset+settings.PAGE_SIZE]
    if not request.is_ajax():
        return render(
            request, "full_list.html", dictionary = {
                "article_list": articles,
            }
        )
    else:
        return render(
            request, "ajax_list.html", dictionary = {
                "article_list": articles,
            }
        )
        #json_serializer = serializers.get_serializer( "json" )
        #return HttpResponse(
        #    json_serializer.serialize( articles ),
        #    content_type = "application/json"
        #)
    
        
