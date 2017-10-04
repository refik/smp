from django.http import HttpResponse
from django.template import loader
from .models import App

def app_list(request):
    app_list = App.objects.all()
    template = loader.get_template("mvp/app_list.html")

    context = {
        'app_list' : app_list
    }

    return HttpResponse(template.render(context, request))

def app(request, app_id):
    app = App.objects.get(pk = app_id)
    template = loader.get_template("mvp/app.html")

    context = {
        'app' : app
    }

    return HttpResponse(template.render(context, request))