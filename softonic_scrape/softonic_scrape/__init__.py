import os
import sys
import django

sys.path.insert(0, '/Users/refik/PycharmProjects/mydownloadfree/mydownloadfree_django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mydownloadfree_django.settings'
django.setup()