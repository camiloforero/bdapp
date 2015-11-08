import gspread
import itertools
import json
from oauth2client.client import SignedJwtAssertionCredentials
from bam.models import LC, Semana, Puntajes

areas =["IGCDP", "OGCDP", "IGIP", "OGIP"]
areas = ["OGIP"]
semana_actual = 1

def importarDatos():
    json_key = json.load(open('google_private.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    gc = gspread.authorize(credentials)
    bam = gc.open_by_key("1v625TZDYgzWn0yYLEUKVtx3CpliMq0rMRQOuFwhv3U0")
    for area in areas:
        wks = bam.worksheet(area)
        LCs = wks.col_values(2)
        puntajes = wks.col_values(2+6*semana_actual)
        puntajes_ip = wks.col_values(6*semana_actual-1)
        puntajes_ma = wks.col_values(6*semana_actual)
        puntajes_bonus = wks.col_values(6*semana_actual+1)
        tuples = itertools.izip_longest(LCs, puntajes, puntajes_ip, puntajes_ma, puntajes_bonus, fillvalue=0)
        print tuples
        for tuple in tuples:
            if tuple[0] and tuple[0].startswith("AIESEC"):
                semana, created = Semana.objects.get_or_create(id=semana_actual)
                lc, created = LC.objects.get_or_create(nombre=tuple[0])
                puntajes, created = Puntajes.objects.get_or_create(semana=semana, lc=lc)
                setattr(puntajes, "%s"%area, tuple[1])
                setattr(puntajes, "ip_%s"%area, tuple[2])
                setattr(puntajes, "ma_%s"%area, tuple[3])
                setattr(puntajes, "bonus_%s"%area, tuple[4])
                puntajes.save()
            print tuple




