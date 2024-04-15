from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Favourite
from .forms import Signup, Login
import yfinance as yi
from django.contrib.auth import authenticate, login, logout
import json

# Create your views here.

def home(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render(request=request))

def market_data(request, azione = None, data_inizio = None, data_fine = None):
    # Prendo il template
    template = loader.get_template('market_data.html')
    '''
    Se ho questi parametri non vuoti, vuol dire che sono stato reindirizzato qui
    dalla pagina dei preferiti (vedesi link nella tabella)
    '''
    if azione != None and data_inizio != None and data_fine != None:
        # Quindi preparo i dati da poi mettere nel form della pagina dei preferiti
        data = dict(azione=azione, data_inizio=data_inizio, data_fine=data_fine)
        return HttpResponse(template.render({"data": data}, request))
    
    # Altrimenti renderizzo il template senza nessun dato
    return HttpResponse(template.render(request=request))

def get_data(request, azione, data_inizio, data_fine):
    print(azione)
    # Scarico i dati tramite la libreria yfinance
    data = yi.download(azione, start=data_inizio, end=data_fine)
    print(data)
    # Li converto in json per mandarli come risposta alla fetch di JS
    json = data.to_json(orient = "index")
    return HttpResponse(json)

def signup(request):
    template = loader.get_template('signup_login.html')
    main = loader.get_template('main.html')

    '''
    Se il metodo della richiesta è la POST, vuol dire che si sono
    mandati dei dati da uno dei due form
    '''
    if request.method == 'POST':
        # Se l'utente si è voluto loggare
        if request.POST.get('submit') == 'login':
            print("login")
            form = Login(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                print(username, password)
                # Uso la funzione di Django per autenticare l'utente
                user = authenticate(request, username=username, password=password)
                print(user)
                # Se mi restituisce un utente vuol dire che ha avuto successo
                if user:
                    # Quindi eseguo il login e reindirizzo l'utente alla home
                    login(request, user)    
                    return redirect('home')
                else:
                    # Altrimenti si sono sbagliate le credenziali e si riporta l'errore alla stessa pagina
                    return HttpResponse(template.render({'error': 'Credenziali Errate'}, request))
            else:
                print(form.errors)
        else:
            # Altrimenti l'utente si vuole registrare
            print("signup")
            form = Signup(request.POST)
            if form.is_valid():
                # Se il form è valido salvo i dati nel database
                form.save()
                # Reindirizzo anche qui l'utente alla home
                return HttpResponse(main.render())
            else:
                print(form.errors.values())
    else:
        form = Signup()
    
    # Altrimenti vuol dire che l'utente ha voluto solo visualizzare la pagina dalla home e quindi viene renderizzata
    return HttpResponse(template.render({'form': form }, request))

# Eseguo il logout e reindirizzo l'utente alla home
def do_logout(request):
    logout(request)
    return redirect('home')

def favourite(request):
    # Faccio visualizzare la pagina solo se l'utente che ha fatto la richiesto è attualmente autenticato
    if request.user.is_authenticated:
        # Prendo tutti i preferiti dell'utente corrente
        favs = Favourite.objects.filter(username = request.user.username)
        template = loader.get_template('favourite.html')
        # Li mando alla pagina html
        return HttpResponse(template.render({'favs': favs}, request))

def add_favourite(request, azione, data_inizio, data_fine):
    # Se il metodo della richiesta è POST e l'utente è autenticato posso aggiungere i dati tra i preferiti dell'utente
    if request.method == "POST" and request.user.is_authenticated:
        try:
            # Verifico se c'è già un preferito con gli stessi dati
            Favourite.objects.get(asset = azione, dataInizio = data_inizio, dataFine = data_fine, username = request.user.username)
            # Se c'è restituisco alla richiesto lo stato che è già presente
            return HttpResponse(json.dumps({"status": "is_present"}))
        except:
            # Altrimenti verrà sollevata un'eccezione dato che la 'get' non avrà trovato niente

            # Quindi scarico i dati richiesti
            data = yi.download(azione, start=data_inizio, end=data_fine)
            # Questo perchè devo verificare se esistono dei dati per l'asset richiesto

            # Se la lunghezza dei dati è 0 vuol dire che l'asset specificato dall'utente non è corretto
            if len(data) == 0:
                # Restituisco l'errore nella risposta
                return HttpResponse(json.dumps({"status": "no_data"}))
            else:
                # Altrimenti i dati sono vali e posso creare un oggetto con i dati seleziona dall'utente e con il suo username
                fav = Favourite(asset = azione, dataInizio = data_inizio, dataFine = data_fine, username = request.user.username)
                # E salvo l'oggetto nel database
                fav.save()
                # Restituisco lo stato di successo
                return HttpResponse(json.dumps({"status": "saved"}))
        
def delete_favourite(request, id):
    # Posso eliminare un preferito solo se l'utente è loggato
    if request.user.is_authenticated:
        # Prendo l'oggetto con lo stesso id della richiesta
        fav = Favourite.objects.get(id = id)
        # Lo elimino
        fav.delete()
        # Reindirizzo l'utente sempre alla pagina dei preferiti
        return redirect('favourite')
