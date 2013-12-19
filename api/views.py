from django.http import HttpResponse
from api.models import Entry
import simplejson
import re
from django.db.models import Q

def search(request, search_term):
    search_term = search_term.lower()
    entries = Entry.objects.filter(esearch=search_term)
    closest_search_term = search_term
    # try to guess singular form
    if len(entries) == 0:
        p1 = re.compile('([a-zA-Z]+?)(es\Z)') # ends with es
        p2 = re.compile('([a-zA-Z]+?)(ss\Z)') # ends with ss
        p3 = re.compile('([a-zA-Z]+?)(s\Z)') # ends with s
        p4 = re.compile('([a-zA-Z]+?)(ed\Z)') # ends with ed
        p5 = re.compile('([a-zA-Z]+?)(ing\Z)') # ends with ing
        p6 = re.compile('([a-zA-Z]+?)(ies\Z)') # ends with ies
        if len(p1.findall(search_term)) > 0:
            closest_search_term = p1.findall(search_term)[0][0]
            entries = Entry.objects.filter(esearch=closest_search_term)
        # end with s but not ss
        if len(entries) == 0 and len(p2.findall(search_term)) == 0 and len(p3.findall(search_term)) > 0:
            closest_search_term = p3.findall(search_term)[0][0]
            entries = Entry.objects.filter(esearch=closest_search_term)
        # ends with ed
        if len(entries) == 0 and len(p4.findall(search_term)) > 0:
            entries = Entry.objects.filter(Q(esearch=search_term[:len(search_term)-1]) | Q(esearch=search_term[:len(search_term)-2]) | Q(esearch=search_term[:len(search_term)-3]))
            entryLength = 0
            tempEntries = []
            # take longest search term as the correct one
            for entry in entries:
                if len(entry.esearch) > entryLength:
                    tempEntries = []
                    tempEntries.append(entry)
                    entryLength = len(entry.esearch)
                    closest_search_term = entry.esearch
                elif len(entry.esearch) == entryLength:
                    tempEntries.append(entry)
            entries = tempEntries
        # ends with ing
        if len(entries) == 0 and len(p5.findall(search_term)) > 0:
            entries = Entry.objects.filter(Q(esearch=search_term[:len(search_term)-3]) | Q(esearch=search_term[:len(search_term)-4]) | Q(esearch=search_term[:len(search_term) - 3] + "e"))
            entryLength = 0
            tempEntries = []
            # take longest search term as the correct one
            for entry in entries:
                if len(entry.esearch) > entryLength:
                    tempEntries = []
                    tempEntries.append(entry)
                    entryLength = len(entry.esearch)
                    closest_search_term = entry.esearch
                elif len(entry.esearch) == entryLength:
                    tempEntries.append(entry)
            entries = tempEntries
        # ends with ies
        if len(entries) == 0 and len(p6.findall(search_term)) > 0:
            closest_search_term = search_term[:len(search_term)-3] + "y"
            entries = Entry.objects.filter(esearch=closest_search_term)

    found = True if len(entries) > 0 else False
    definitions = []
    for (counter, entry) in enumerate(entries):
        definitions.append(entry.tentry)

    data = {"found" : found, "search_term" : search_term, "closest_search_term" : closest_search_term, "definitions" : definitions}

    return HttpResponse(simplejson.dumps(data), content_type='application/json',)