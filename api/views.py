from django.http import HttpResponse
from api.models import Entry
from django.shortcuts import render

def search(request, search_term):
    entry = Entry.objects.filter(esearch=search_term)

    return HttpResponse("Your search term is " + search_term)