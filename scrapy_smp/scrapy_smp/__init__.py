import os
import sys
import django

sys.path.insert(0, '/Users/refik/PycharmProjects/mydownloadfree/django_smp')
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_smp.settings'
django.setup()