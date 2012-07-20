from django.conf import settings
import datetime
def utcnow(request):
    return {'utcnow': datetime.datetime.utcnow()}
