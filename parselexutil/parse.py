"""
Parse NECTEC's xml definition file and insert into dynamodb database.
This is a one-off script to populate the English-Thai definition for the firs time.
"""
import os
from xml.dom import minidom

import boto3


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

dir_path = os.path.dirname(os.path.realpath(__file__))
xmldoc = minidom.parse(dir_path + '/etlex.xml')
itemlist = xmldoc.getElementsByTagName('entry')

print("done parsing")

item = itemlist[0]
for item in itemlist:
    esearch = item.getElementsByTagName('esearch')[0].childNodes[0].data if len(item.getElementsByTagName('esearch')) > 0 and len(item.getElementsByTagName('esearch')[0].childNodes) > 0 else None
    tentry = item.getElementsByTagName('tentry')[0].childNodes[0].data if len(item.getElementsByTagName('tentry')) > 0 and len(item.getElementsByTagName('tentry')[0].childNodes) > 0 else None
    if tentry is None or esearch is None:
        print("IGNORED: tentry " + str(tentry) + " esearch " + str(esearch))
        continue
    if esearch in dict:
        dict[esearch].add(tentry)
    else:
        dict[esearch] = set()
        dict[esearch].add(tentry)

print("done parsing")
dynamodb = boto3.resource('api', region_name='ap-southeast-1')
table = dynamodb.Table('english_thai_dict_v2')
keys = list(dict.keys())
for chunk in chunks(keys, 50):
    print("Chunk " + str(chunk))
    for key in chunk:
        with table.batch_writer() as batch:
            batch.put_item(
                Item={
                    'english_word': key,
                    'thai_definitions': dict[key]
                }
            )