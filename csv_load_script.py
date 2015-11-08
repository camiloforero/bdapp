from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

import csv
import urllib2

reader = None

def loadDocument():
    with open('aplicantes.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            print row

def cargarTrainees():
    if reader == None:
        loadDocument()
    response = urllib2.urlopen(reader[0]["cv"])
    tempfile = NamedTemporaryFile(delete=True)
    tempfile.write(response.read())
    tempfile.flush()
    return tempfile
