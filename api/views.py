from django.http import HttpResponse
from api.models import Entry
import simplejson
import re

def search(request, search_term):
    search_term = search_term.lower()
    entries = Entry.objects.filter(esearch=search_term)
    closest_search_term = search_term
    if len(entries) == 0:
        p1 = re.compile('([a-zA-Z]+?)(es\Z)')
        p2 = re.compile('([a-zA-Z]+?)(ss\Z)')
        p3 = re.compile('([a-zA-Z]+?)(s\Z)')
        if len(p1.findall(search_term)) > 0:
            closest_search_term = p1.findall(search_term)[0][0]
            entries = Entry.objects.filter(esearch=closest_search_term)
        if len(entries) == 0 and len(p2.findall(search_term)) == 0 and len(p3.findall(search_term)) > 0:
            closest_search_term = p3.findall(search_term)[0][0]
            entries = Entry.objects.filter(esearch=closest_search_term)

    found = True if len(entries) > 0 else False
    definitions = []
    for (counter, entry) in enumerate(entries):
        definitions.append(entry.tentry)

    data = {"found" : found, "search_term" : search_term, "closest_search_term" : closest_search_term, "definitions" : definitions}

    return HttpResponse(simplejson.dumps(data), content_type='application/json',)