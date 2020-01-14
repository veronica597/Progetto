/* File js associato a statistics.html */

/*jslint browser: true*/
/*global $, document, console, window */  

/* eslint no-console: 0*/  // per eliminare l'errore "no-console" localmente (per farlo in maniera globale dovrei modificare il file .eslintrc -- dovrei aver scaricato jquery ma io ho usato la CDN)

// servono per eliminare gli errori relativi a $ o JQuery, derivanti dal fatto che $ e JQuery sono create da JQuery al momento del caricamento della pagina --> JSLint che fa code checking le trova non definite, ma il codice funziona lo stesso perche' poi queste variabili sono definite comunque al caricamento della pagina 


var day ;
var month ;
var year ;

var dayF  ;
var monthF ;
var yearF ;


var requestUrl;
var ip = '192.168.1.67'; // indirizzo ip 172.20.10.2, localhost, 192.168.1.67



console.log("tipo year:" +" "+ typeof year);
console.log("tipo month:" +" "+ typeof month);
console.log("tipo day:" +" "+ typeof day);

console.log("tipo yF:" +" "+ typeof yearF);
console.log("tipo mF:" +" "+ typeof monthF);
console.log("tipo dF:" +" "+ typeof dayF);


function pippo(aDiv1,) {
    var e = document.getElementById(aDiv1);

    if (e.style.display == "none") {
        e.style.display = "block"
    }
}

function Pippo(aDiv1,aDiv2,aDiv3,aDiv4) {
    var e = document.getElementById(aDiv1);
    var b= document.getElementById(aDiv2);
    var c= document.getElementById(aDiv3);
    var v= document.getElementById(aDiv4);

    b.style.display="inline"; // tengo bloccato menu tendina

    if (v.style.display=="block" ){ // scompare input altro tasto
        v.style.display="none";
    }


    if(c.style.display=="block" ){ // scompare alert
        c.style.display="none";
    }


    if (e.style.display == "none") { //mostro input
        e.style.display = "block"
    }
}

// SCRIPT PER I DUE DATETIMEPICKER
$('#datepickerI'),$('#datepickerF'),$('#datepickerI1').datepicker({
    weekStart: 1,
    daysOfWeekHighlighted: "6,0",
    autoclose: true,
    todayHighlight: true,
});

$(function() {
    $('#datepickerI').datepicker();
    $('#datepickerF').datepicker();
    $('#datepickerI1').datepicker();

    $("#datepickerI1").on("change", function () {  // per selezione giorno singolo 
        day = $(this).datepicker('getDate').getDate();
        month = $(this).datepicker('getDate').getMonth() + 1;
        year = $(this).datepicker('getDate').getFullYear();
        console.log(day);
        console.log(month);
        console.log(year);

        requestUrl = "http://" + ip + ":8000/dispenser/fake/?anno=" + year + "&mese=" + month + "&giorno=" + day + "";


        $.get(requestUrl, function (data) {
            console.log('DATI RICEVUTI: ' + data);
            if (data == 0) {
                var l= document.getElementById('mioAlert');
                l.style.display='block';
            } 
            else {
                window.location.href="http://" + ip + ":8000/dispenser/dati/?anno=" + year + "&mese=" + month + "&giorno=" + day + "";
            }


            });

    });


    $("#datepickerI").on("change", function () {
        day = $(this).datepicker('getDate').getDate();
        month = $(this).datepicker('getDate').getMonth() + 1;
        year = $(this).datepicker('getDate').getFullYear();
        console.log(day);
        console.log(month);
        console.log(year);

        $("#datepickerF").removeAttr("disabled"); // riattivo secondo calendario

        console.log("tipo yeaar" + " " + typeof year);

        console.log("tipo yearF" + " " + typeof yearF);


    });




    $("#datepickerF").on("change", function (){

        dayF = $(this).datepicker('getDate').getDate();
        monthF = $(this).datepicker('getDate').getMonth() + 1;
        yearF = $(this).datepicker('getDate').getFullYear();

        console.log(dayF);
        console.log(monthF);
        console.log(yearF);

        console.log("tipo year2" +" "+ typeof year);
        console.log("tipo yearF2" +" "+ typeof yearF);
        caricamento();
    });


});

function caricamento() {
    if(year == yearF && month== monthF && day == dayF) {  // caso in cui seleziono la stessa data nelle due celle 
        console.log(" Mostro giorno scelto dal primo cal");
        requestUrl = "http://" + ip + ":8000/dispenser/fake/?anno=" + year + "&mese=" + month + "&giorno=" + day + "";

        $.get(requestUrl, function (data) {
            console.log('DATI RICEVUTI: ' + data);
            if (data == 0) {
                var l= document.getElementById('mioAlert2');
                l.style.display='block';

            }

            else {
                window.location.href="http://" + ip + ":8000/dispenser/dati/?anno=" + year + "&mese=" + month + "&giorno=" + day + "";

            }

        });

    } 

   else{
        console.log(" Ho sel anche sul sec calendario. Mostro periodo selezionato! ");
        requestUrl = "http://" + ip +":8000/dispenser/fakeP/?anno=" + year + "&mese=" + month + "&giorno=" + day + "&annoF=" + yearF + "&meseF=" + monthF + "&giornoF=" + dayF + "";

        $.get(requestUrl, function (data) {
             console.log('DATI RICEVUTI: ' + data);
            if (data == 0) {
                var l= document.getElementById('mioAlert2');
                l.style.display='block';

            }else {
                 window.location.href = "http://" + ip + ":8000/dispenser/statistic/?id=2" + "&anno=" + year + "&mese=" + month + "&giorno=" + day + "&annoF=" + yearF + "&meseF=" + monthF + "&giornoF=" + dayF + "";



            }
         });


    }
}



// funzione per verificare la presenza di dati per la SETTIMANA piu' recente

function dataAvailableS(){

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


            //window.location.href="http://" + ip + ":8000/dispenser/statistic/?id=0&noData=1"; 
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

//funzione per verificare la presenza di dati per la MESE piu' recente

function dataAvailableM(){

    console.log("dentro la funzione"); 
    requestUrl = "http://" + ip + ":8000/dispenser/fakeSM/?id=1"; 

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



            window.location.href="http://" + ip + ":8000/dispenser/statistic/?id=1&noData=1" + "&anno=" + yearS + "&mese=" + monthS + "&giorno=" + dayS + "&annoF=" + yearE + "&meseF=" + monthE + "&giornoF=" + dayE + "";  


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


            window.location.href="http://" + ip + ":8000/dispenser/statistic/?id=1" + "&noData=0" + "&anno=" + yearS + "&mese=" + monthS + "&giorno=" + dayS + "&annoF=" + yearE + "&meseF=" + monthE + "&giornoF=" + dayE + "";
        }
    }); 
}

