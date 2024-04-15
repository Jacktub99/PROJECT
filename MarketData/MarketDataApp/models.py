from django.db import models

# Create your models here.

'''
Come unico modello nel database, oltre agli utenti, ho una
tabella che salva i preferiti, ogni preferito è identificato
da un id che è quindi la chiave primaria nella tabella, e dai
dati che identificano l'utente, e il tipo di asset che si è salvato
'''
class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    asset = models.CharField(max_length=100)
    dataInizio = models.CharField(max_length=100)
    dataFine = models.CharField(max_length=100)