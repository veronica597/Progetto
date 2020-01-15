/* File js associato a getPost.html */

/*jslint browser: true*/
/*global $, document, console, window */  

/* eslint no-console: 0*/  // per eliminare l'errore "no-console" localmente (per farlo in maniera globale dovrei modificare il file .eslintrc -- dovrei aver scaricato jquery ma io ho usato la CDN)

// servono per eliminare gli errori relativi a $ o JQuery, derivanti dal fatto che $ e JQuery sono create da JQuery al momento del LoadDataSelected della pagina --> JSLint che fa code checking le trova non definite, ma il codice funziona lo stesso perche' poi queste variabili sono definite comunque al LoadDataSelected della pagina

function show(aDiv1,) {
    var e = document.getElementById(aDiv1);

    if (e.style.display == "none") {
        e.style.display = "block"
    }
}

function showForTables(aDiv1, aDiv2) {
    var e = document.getElementById(aDiv1);
    var e2 = document.getElementById(aDiv2);
    if (e.style.display == "block") {
        e.style.display = "none";
        e2.style.display = "block";
    }
}


function notShow(aDiv1,) {
    var e = document.getElementById(aDiv1);

    if (e.style.display == "block") {
        e.style.display = "none"
    }
}


console.log("pronti alla get");

// var ip = "192.168.1.67"; // 172.20.10.2, localhost, 192.168.1.67
var ip = 'localhost';

var DEVICE_IP = '192.168.1.128'; // indirizzo IP della scheda ESP8266 --172.20.10.5

function servoOn(){
    console.log("click sul bottone 'Ruota il servo'");
    var requestUrl = "http://" + DEVICE_IP + "/servoOpen";
    $.get(requestUrl, function(){
        //alert("sto facendo una get all'ESP8266");
        console.log("sto facendo una get all'ESP8266"); 
    });

}


// funzione per verificare la presenza di dati per la SETTIMANA piu' recente

function dataAvailableW(){

    console.log("dentro la funzione"); 
    requestUrl = "http://" + ip + ":8000/dispenser/fakeWM/?id=0";

    $.get(requestUrl, function (data) {
        console.log('DATI RICEVUTI: ' + data);
        if(data[0] == 0){
            console.log("alert a tutta pagina");
            // mi sposto sulla pagina /statistic cmq

            // recupero la data di inizio e di fine del Period
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

            //window.location.href="http://" + ip + ":8000/dispenser/statistic/?id=0&noData=1"; 

            window.location.href="http://" + ip + ":8000/dispenser/statistic/?id=0&noData=1" + "&anno=" + yearS + "&mese=" + monthS + "&giorno=" + dayS + "&annoF=" + yearE + "&meseF=" + monthE + "&giornoF=" + dayE + "";

        }
        else{ // renderizzo i dati che ci sono normalmente 

            // recupero la data di inizio e di fine del Period
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

//funzione per verificare la presenza di dati per la MESE piu' recente

function dataAvailableM(){

    console.log("dentro la funzione"); 
    requestUrl = "http://" + ip + ":8000/dispenser/fakeWM/?id=1";

    $.get(requestUrl, function (data) {
        console.log('DATI RICEVUTI: ' + data);
        if(data[0] == 0){
            console.log("alert a tutta pagina");
            
            // recupero la data di inizio e di fine del Period
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


            //window.location.href="http://" + ip + ":8000/dispenser/statistic/?id=1&noData=1"; 
            window.location.href="http://" + ip + ":8000/dispenser/statistic/?id=1&noData=1" + "&anno=" + yearS + "&mese=" + monthS + "&giorno=" + dayS + "&annoF=" + yearE + "&meseF=" + monthE + "&giornoF=" + dayE + "";  
             

        }
        else{ // renderizzo i dati che ci sono normalmente 

            // recupero la data di inizio e di fine del Period
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


            window.location.href="http://" + ip + ":8000/dispenser/statistic/?id=1" + "&noData=0" + "&anno=" + yearS + "&mese=" + monthS + "&giorno=" + dayS + "&annoF=" + yearE + "&meseF=" + monthE + "&giornoF=" + dayE + "";
        }
    }); 
}