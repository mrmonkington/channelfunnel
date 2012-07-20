from django.core.management.base import BaseCommand
import os, sys
from django.conf import settings
from pprint import pprint
import logging
from content.models import Source, Article

import feedparser
from datetime import datetime

from weightedngram import NGram

from collections import defaultdict

import operator
import math

#class NGramArticle( NGram ):
#    def iconv( item ):
#        return unicode( item )

import re

class Command( BaseCommand ):

    def handle( self, *args, **options ):

        def enrich( obj ):
            #s = unicode( obj ).lower()
            s = obj.strip().lower()
            # simple stop words
            s = re.sub( r"\b(the|of|in|a)\b", "", s, re.IGNORECASE )
            # type prefixes
            s = re.sub( r"^(trailer|review|report|screenshots|video):\s*", "", s, re.IGNORECASE )
            return s

        trigrams = defaultdict(int)

        for ln in sys.stdin:
            n = NGram( warp=2.5, iconv=enrich, N=3 )
            s = n.iconv( ln )
            s = n.pad( s )
            for gram in n.ngrams( s ):
                trigrams[gram] += 1

        
        max_idf = math.sqrt(math.log(float(len(trigrams))/1.0))
        #print len(trigrams)
        #return
        # set weights to sqrt(log(N/n))
        for word in trigrams.keys():
            # 1.0 constant to account for missing words
            #trigrams[word] = math.sqrt(math.log(float(len(trigrams))/(1.0+trigrams[word])))
            # normalize
            trigrams[word] = math.sqrt(math.log(float(len(trigrams))/(1.0+trigrams[word])))/max_idf

        # (missing trigram) value
        trigrams['$$$'] = 1.0
        import pprint            
        pprint.pprint( sorted(trigrams.iteritems(), key=operator.itemgetter(1)) )

