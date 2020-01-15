/* File js associato a index.html */

/*jslint browser: true*/
/*global $, document, console, window */  

/* eslint no-console: 0*/  // per eliminare l'errore "no-console" localmente (per farlo in maniera globale dovrei modificare il file .eslintrc -- dovrei aver scaricato jquery ma io ho usato la CDN)

// servono per eliminare gli errori relativi a $ o JQuery, derivanti dal fatto che $ e JQuery sono create da JQuery al momento del caricamento della pagina --> JSLint che fa code checking le trova non definite, ma il codice funziona lo stesso perche' poi queste variabili sono definite comunque al caricamento della pagina 


console.log("CIAO");
var ip = '192.168.1.67'; // 172.20.10.2 , localhost, 192.168.1.67


/* funzione per verificare la presenza di dati per la settimana piu' recente*/

function dataAvailable(){
    console.log("dentro la funzione"); 
    requestUrl = "http://" + ip + ":8000/dispenser/fakeSM/?id=0"; // di default voglio sapere se ci sono dati per l'ultima settimana 

    $.get(requestUrl, function (data) {
        console.log('DATI RICEVUTI: ' + data);
        if(data[0] == 0){
            console.log("alert a tutta pagina");
            // mi sposto sulla pagina /statistic cmq

            // recupero la data di inizio e di fine del periodo
            var start = new Date(data[1]); // passato 
            var end = new Date(data[2]); // oggi 

            var yearS = start.getFullYear();
            var monthS = start.getMonth() + 1; 
            var dayS = start.getDate(); 

            var yearE = end.getFullYear();
            var monthE = end.getMonth() + 1;
            var dayE = end.getDate();

            console.log("START: " + yearS + " " + monthS + " " + dayS + " "); 

            console.log("END: " + yearE + " " + monthE + " " + dayE + " "); 


            window.location.href="http://" + ip + ":8000/dispenser/statistic/?id=0&noData=1" + "&anno=" + yearS + "&mese=" + monthS + "&giorno=" + dayS + "&annoF=" + yearE + "&meseF=" + monthE + "&giornoF=" + dayE + "";


        }
        else{ // renderizzo i dati che ci sono normalmente 

            // recupero la data di inizio e di fine del periodo
            var start = new Date(data[1]); // passato 
            var end = new Date(data[2]); // oggi 

            var yearS = start.getFullYear();
            var monthS = start.getMonth() + 1; 
            var dayS = start.getDate(); 

            var yearE = end.getFullYear();
            var monthE = end.getMonth() + 1;
            var dayE = end.getDate();

            console.log("START: " + yearS + " " + monthS + " " + dayS + " "); 

            console.log("END: " + yearE + " " + monthE + " " + dayE + " "); 


            window.location.href="http://" + ip + ":8000/dispenser/statistic/?id=0" + "&noData=0" + "&anno=" + yearS + "&mese=" + monthS + "&giorno=" + dayS + "&annoF=" + yearE + "&meseF=" + monthE + "&giornoF=" + dayE + "";
        }
    }); 
}


