import pprint

from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Sum
from stream_records.models import StreamingRecord
from django.template import loader

from .models import StreamingRecord


def index(request):
    # Get the top 3 highest grossing services
    top_services = (StreamingRecord.objects.values('service_name')
                       .annotate(total_payout=Sum('amount'))
                       .order_by('-total_payout')[:3])

    context = {"top_services": top_services}

    return render(request, "stream_records/index.html", context)



def detail(request, id):
    return HttpResponse("You're looking at question %s." % id)
