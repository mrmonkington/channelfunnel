python manage.py sqlreset content | python manage.py dbshell
python manage.py syncdb
python manage.py loaddata content < content/fixtures/content.json
