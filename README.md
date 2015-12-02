# Channel Funnel

A simple news aggregator that n-gram clusters stories and presents them
in a simple, infinite-scroll view.  Written in Python using Django and
a few other bits.

Designed to work with news feeds from gaming sites, so some of the
normalisation is tailored to that kind of content.

## Installation

```
pip install -r requirements.txt
cp settings/dev-example.py settings/dev.py
python manage.py syncdb
python manage.py runserver
```

Visit [[http://127.0.0.1:8000/admin/]] and add some RSS sources under content/sources.

Scrape:

```
python manage.py scrape
```

Check out some clusters [[http://127.0.0.1:8000/clustertitle/]] and stuff.
