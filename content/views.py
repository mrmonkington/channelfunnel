from models import *
from django.shortcuts import render
from django.core import serializers

def home( request ):
    offset = request.GET.get( "offset", 0 )
    articles = Article.objects.filter( status = "live" ).order_by( "-date_published" )[offset:50]
    if not request.is_ajax():
        return render(
            request, "list.html", dictionary = {
                "article_list": articles,
            }
        )
    else:
        json_serializer = serializers.get_serializer( "json" )
        return HttpResponse(
            json_serializer.serialize( articles ),
            content_type = "application/json"
        )
    
        
