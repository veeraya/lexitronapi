from django.http import HttpResponse
from api.models import Entry
from django.shortcuts import render

def search(request, search_term):
    entries = Entry.objects.filter(esearch=search_term)
    definition = ""
    for (counter, entry) in enumerate(entries):
        definition += str(counter) + ". " + entry.tentry + " "
    return HttpResponse("Definition: " + definition)