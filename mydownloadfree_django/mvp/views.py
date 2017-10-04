from django.http import HttpResponse
from django.template import loader
from .models import App

def index(request):
    app = App.objects.all()[10]
    template = loader.get_template("mvp/app.html")

    context = {
        'app' : app
    }

    return HttpResponse(template.render(context, request))