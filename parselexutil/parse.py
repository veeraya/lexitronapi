# parse the xml definition file and insert into database
from xml.dom import minidom
import MySQLdb

xmldoc = minidom.parse('eltex.xml')
itemlist = xmldoc.getElementsByTagName('entry')

print "done parsing"

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="root", # your password
                      db="lexitron") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the query you need
cur = db.cursor()
db.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')
print "connection successful"

item = itemlist[0]
for item in itemlist:
    id = item.getElementsByTagName('id')[0].childNodes[0].data

    esearch = item.getElementsByTagName('esearch')[0].childNodes[0].data if len(item.getElementsByTagName('esearch')) > 0 and len(item.getElementsByTagName('esearch')[0].childNodes) > 0  else ""
    eentry = item.getElementsByTagName('eentry')[0].childNodes[0].data if len(item.getElementsByTagName('eentry')) > 0 and len(item.getElementsByTagName('eentry')[0].childNodes) > 0  else ""
    tentry = item.getElementsByTagName('tentry')[0].childNodes[0].data if len(item.getElementsByTagName('tentry')) > 0 and len(item.getElementsByTagName('tentry')[0].childNodes) > 0  else ""
    ecat = item.getElementsByTagName('ecat')[0].childNodes[0].data if len(item.getElementsByTagName('ecat')) > 0 and len(item.getElementsByTagName('ecat')[0].childNodes) > 0  else ""
    cur.execute("INSERT INTO api_entry (esearch, eentry, tentry, ecat, id) VALUES (%s, %s, %s, %s, %s)", (esearch, eentry, tentry, ecat, id))

db.commit()
cur.close()
db.close()