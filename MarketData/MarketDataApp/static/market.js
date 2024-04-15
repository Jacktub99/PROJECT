//Prendo il canvas e imposto le dimensioni
var ctx = document.getElementById('chart').getContext('2d');
ctx.canvas.width = 1200;
ctx.canvas.height = 500;

//Prendo gli oggetti che rappresentano gli input delle date
let dataInizio = document.getElementById("min-date");
let dataFine = document.getElementById("max-date");

//Imposto come opzioni da passare al metodo toLocaleString il formato in cui voglio le date in modo tale che siamo compatibili col formato di Python
const options = {
    year: "numeric",
    month: "numeric",
    day: "numeric",
};

//Imposto come valore massimo iniziale che possono assumere i due input la data di oggi
dataFine.max = new Date(Date.now()).toLocaleString("sv-SE", options);
dataInizio.max = new Date(Date.now()).toLocaleString("sv-SE", options);

//Se quando viene caricata la pagina uno degli input ha già un valore all'interno vuol dire
//che arrivo dai preferiti e Django mi ha passato già i valori, quindi devo chiamare la funzione 
//'add()' per ottenere i dati e visualizzarli sul grafico
if (dataInizio.value) add();

//Funzione che viene chiamata quando si preme sul bottone della stella per aggiungere la tripla
//(asset, dataInizio, dataFine) ai preferiti per l'utente corrente
function addFavourite() {
    console.log(csrftoken);
    //Ottengo i dati dagli input
    azione = document.getElementById("input-simbolo").value;
    minDate = document.getElementById("min-date").value;
    maxDate = document.getElementById("max-date").value;
    //Creo la richiesta da mandare al backend di Django, deve essere una POST, e nell'header della richiesta
    //specifico anche il csrftoken passato quando è stata renderizzata la pagina per far in modo che la richiesta
    //vada a buon fine, altrimenti viene restituito errore
    fetch(`/add-favourite/${azione}/${minDate}/${maxDate}`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
        .then(response => {
            //Se riesco ad ottenere la risposta la converto in JSON
            if (!response.ok) {
                throw new Error('Errore durante la richiesta');
            }
            return response.json();
        })
        .then(data => {
            //Adesso ottengo l'oggetto dell'alert e rimuovo tutte le classi precedenti che impostano il colore
            let alert = document.getElementById("alert-market");
            alert.classList.remove("alert-success", "alert-danger");
            console.log(data);

            //Se la risposta è positiva ("saved")
            if (data["status"] == "saved") {
                //Imposto il messaggio di successo negli elementi all'interno l'alert
                document.getElementById("strong-alert").innerText = "Ottimo!";
                document.getElementById("text-alert").innerText = "Asset aggiunto con successo ai preferiti.";
                //Aggiungendo la classe 'show' all'alert Bootstrap lo mostrerà all'utente
                alert.classList.add("alert-success", "show");
            } else if (data["status"] == "is_present") {
                //Se l'asset con le stesse date è già presente nel DB stampo l'errore
                document.getElementById("strong-alert").innerText = "Errore!";
                document.getElementById("text-alert").innerText = "Asset con lo stesso intervallo di date già presente nei preferiti.";
                //Con la classe 'alert-danger' l'alert verrà colorato di rosso
                alert.classList.add("alert-danger", "show");
            } else {
                //L'ultimo caso si verifica se l'asset inserito dall'utente non restituisce nessun risultato,
                //In questo caso verrà impostato un messaggio di errore generico che imposto nella seguente funzione
                assetError(alert);
            }

            //Alla fine faccio scomparire l'alert dopo 5 secondi rimuovendo la classe 'show' (può anche scomparire prima se l'utente clicca sul bottone 'close' dell'alert)
            setTimeout(() => {
                alert.classList.remove("show");
            }, 5000);
        })
        .catch(error => {
            console.error('Errore durante la richiesta:', error);
        });
}

//Messaggio di errore standard per l'alert
function assetError(alert) {
    document.getElementById("strong-alert").innerText = "Errore!";
    document.getElementById("text-alert").innerText = "Nessun Asset Trovato.";
    alert.classList.add("alert-danger", "show");
}

//Funzione per cambiare la data minima che può avere la data di fine, che non può essere
//antecedente a quella di inizio
function cambioMax() {
    dataFine.min = dataInizio.value;
}

//Funzione per cambiare la data massima che può avere la data di inizio, che non può essere
//successiva a quella di fine
function cambioMin() {
    dataInizio.max = dataFine.value;
}

//Creo il grafico inizialmente senza dati
var chart = new Chart(ctx, {
    type: 'candlestick',
    data: {
        datasets: [{
            label: 'Data',
            data: [], //All'inizio i dati sono vuoti
            borderColor: 'rgba(255, 99, 132, 1)', //Colore del bordo
            backgroundColor: 'rgba(255, 99, 132, 0.5)', //Colore di riempimento
        }]
    }
});

//Funzione per aggiungere dati al grafico
function add() {
    //Ottengo i dati dagli input
    azione = document.getElementById("input-simbolo").value;
    minDate = document.getElementById("min-date").value;
    maxDate = document.getElementById("max-date").value;
    console.log(azione, minDate, maxDate);
    //Mando la richiesta al backend Django
    fetch(`/get-data/${azione}/${minDate}/${maxDate}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore durante la richiesta');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            //Se la lunghezza dei dati è 0 vuol dire che ho inserito un asset sbagliato e viene mostrato un alert di errore
            if (Object.keys(data).length == 0) {
                let alert = document.getElementById("alert-market");
                alert.classList.remove("alert-success", "alert-danger");
                alert.classList.add("alert-danger", "show");

                assetError(alert);

                setTimeout(() => {
                    alert.classList.remove("show");
                }, 5000);
            } else {
                //Altrimenti i dati inseriti sono corretti e posso popolare l'array che rappresenta i dati
                let barData = []
                for (let date in data) {
                    barData.push({
                        x: Number.parseInt(date), //Converto la data in un numero dato che la libreria chart.js richiede questo formato
                        o: data[date]['Open'],
                        h: data[date]['High'],
                        l: data[date]['Low'],
                        c: data[date]['Close'],
                    });
                }
                console.log(barData);
                //Accedo al primo (e unico) dataset del grafico (con [0]) e aggiorno il campo 'data' con i dati appena formattati
                chart.config.data.datasets[0].data = barData;
                //Chiamo la funzione 'update()' sul grafico per mostrare i cambiamenti nel canvas
                chart.update();
            }
        })
        .catch(error => {
            console.error('Errore durante la richiesta:', error);
        });
}