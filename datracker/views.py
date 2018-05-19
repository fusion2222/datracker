from django.template.response import HttpResponse

def index(request):
    return HttpResponse('Works perfectly!')
