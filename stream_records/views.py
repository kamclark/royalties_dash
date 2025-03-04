from django.http import HttpResponse


def index(request):
    name = "USER"
    return HttpResponse(f"Hello {name}! This is a view for records.")
