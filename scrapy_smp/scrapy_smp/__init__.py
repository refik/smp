import os
import sys
import django

django_path = os.getenv("SMP_DJANGO_PATH")
if not django_path:
    raise Exception("SMP_DJANGO_PATH environment variable "
                    "is not defined.")
sys.path.insert(0, django_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_smp.settings'
django.setup()
