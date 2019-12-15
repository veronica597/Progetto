
#include <ArduinoJson.h>
#include <Servo.h>
#include <Time.h>
#include <TimeLib.h>
#include <NTPClient.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <ESP8266HTTPClient.h>


const char *ssid     = "TIM-25165130";
const char *password = "rioneverde46";

//const char* ssid = "MICC_LabR1";
//const char* password = "w1reless!micc!";

//const char *ssid     = "HUAWEI P30 lite";
//const char *password = "nicolino%";

//const char *ssid     = "eduroam";
//const char *password = "Rioneverde46";

const long utcOffsetInSeconds = 7200; // CONTROLLARE ORA LEGALE PER QUANDO CONSEGNAMO PROGETTO -- 3600??

char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};

// Define NTP Client to get time

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "europe.pool.ntp.org", utcOffsetInSeconds); // va bene anche pool.ntp.org -- worldwide

#define PIR_PIN 16 // D0
Servo servo;
WiFiServer server(80);

int calibration_time = 30; // tempo di calibrazione del sensore PIR
int passGiorno = 0;
int passNotte = 0;

// variabili di tempo

unsigned long currentTime;
unsigned long servoTime;
unsigned long letturaDati;
//unsigned long letturaSensore; // per fare tipo "se il segnale e' ancora alto dopo un tot di secondi allora erogo" -- conto le letture del sensore
unsigned long interval; // per gestire gli intervalli di riavvio automatico del servo
unsigned long waitTime; // per gestire gli intervalli di riavvio del servo dopo click dell'utente
unsigned long nightTime;

int currentHour;
int currentMinutes;
int currentSeconds;
int startHour = 17;
int startMinutes = 32;
int stopHour = 17;
int stopMinutes = 34;

bool attivaServo;
int mod = 1; // di default sono in modGiorno
int primoPassaggio;
int pir = 0;
bool var = false; // per la riattivazione del servo dopo la modalita' notte
bool erogazione = false; // per post

bool userMode = false; // per distinguere tra erogazione automatica e volontaria
bool scatto = false; // per riattivazione post click
int countClick = 0; // per evitare che l'utente clicchi due/piu' volte ravvicinatamente
int countClickN = 0; //  per evitare che l'utente clicchi due/piu' volte ravvicinatamente in modalita' notte


void setup() {

  pinMode(PIR_PIN, INPUT);

  servo.attach(2); // D4
  if (servo.attached() == false) {
    Serial.println("errore");
  }
  attivaServo = true;
  servo.write(0); // servo settato a 0°

  Serial.begin(9600);

  // Fase di calibrazione PIR

  Serial.print("Calibrazione del sensore ");
  for (int i = 0; i < calibration_time; i++) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println(" Fatto");
  while (digitalRead(PIR_PIN) == HIGH) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("SENSORE ATTIVO");

  // Connessione alla rete WiFi
  //WiFi.begin(ssid, password);
  WiFi.begin(ssid);

  WiFi.config(IPAddress(192, 168, 1, 128), IPAddress(192, 168, 1, 1), IPAddress(255, 255, 255, 0)); // configurazione indirizzo IP dell'ESP8266 all'interno della LAN
  //WiFi.config(IPAddress(192, 168, 1, 134), IPAddress(192, 168, 0, 1), IPAddress(255, 255, 254, 0)); // MICC
  //WiFi.config(IPAddress(192, 168, 43, 128), IPAddress(192, 168, 43, 3), IPAddress(255, 255, 255, 0)); // HUAWEI P30 lite
  //WiFi.config(IPAddress(172, 22, 36, 128), IPAddress(172, 22, 32, 1), IPAddress(255, 255, 224, 0)); // FirenzeWiFi
  //WiFi.config(IPAddress(172, 17, 196, 174), IPAddress(172, 17, 196, 1), IPAddress(255, 255, 128, 0));

  while ( WiFi.status() != WL_CONNECTED ) {
    delay ( 500 );
    Serial.print ( "." );
  }

  Serial.println("");
  Serial.println("WiFi connesso");

  // Start the server

  server.begin();
  Serial.println("Server attivato");

  // Mostra l'indirizzo IP assegnato

  Serial.print("Utilizza questa URL per connetterti: "); // url del server (= scheda ESP8266)
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");

  timeClient.begin();

  // Setup variabili di tempo

  currentTime = millis();
  interval = millis();
  servoTime = millis();
  letturaDati = millis();
  waitTime = millis();
  nightTime = millis();

}

void loop() {

  currentTime = millis();
  lettura(); // togliere dal loop e mettere nei punti critici del codice

  // Controlla se il client è connesso
  WiFiClient client = server.available();

  if (!client) {
    userMode = false; // modalita' automatica
    if (hourRange(currentHour, currentMinutes, startHour, startMinutes, stopHour, stopMinutes) == true) { //attivaServo == true &&

      mod = 0; // modalita' notte attiva
      modNotte();

    }
    else {

      mod = 1; // modalita' giorno attiva
      modGiorno();

    }
  }

  else {
    userMode = true; // modalita' utente
    userInput(client);
  }

}


void modGiorno() {

  pir = digitalRead(PIR_PIN);

  if (pir == 1 && attivaServo == true) {
    Serial.println("Il sensore ha rilevato un movimento");
    erogazione = true;
    primoPassaggio++;
    passGiorno++;
    Serial.print("passaggi di giorno: ");
    Serial.println(passGiorno);

    //ruoto servo motore

    servo.write(180);
    delay(1000);
    Serial.println(servo.read());

    delay(1000);
    servo.write(0);

    delay(1000);
    Serial.println(servo.read());

    Serial.println("POST");
    postDati(erogazione, userMode, mod);
    //getToView();
    stampaOrario();
  }

  else if (pir == 1 && attivaServo == false) {
    erogazione = false;
    Serial.println("POST");
    postDati(erogazione, userMode, mod);
    //getToView();
    stampaOrario();
    delay(3000);

  }

  if (primoPassaggio == 1 && attivaServo == true) { // temporizzare del tipo -- se sono passati tot ms dal primo passaggio e il servo e' attivo allora ...
    servo.detach();
    if (servo.attached() == false) {
      attivaServo = false;
    }
    Serial.println("Il servo e' stato disattivato");
    var = false;
    interval = millis(); // il "timer" riparte quando erogo
  }

  currentTime = millis();

  if ((attivaServo == false && currentTime > interval + 60000)) { // dopo 1 minuto riattivo il servo
    if (scatto == false) { // se NON c'e' stato un click nell'intervallo di disattivazione
      primoPassaggio = 0;
      servo.attach(2);
      if (servo.attached() == true) {
        attivaServo = true;
        Serial.println("Servo riattivato");
        stampaOrario();
      }

      interval = millis(); // aggiorno interval da qui (in modo automatico) solo se non ho avuto click da parte dell'utente
    }
  } // chiude if(attivaServo == false && ... )

  if (attivaServo == false && var == true) {
    primoPassaggio = 0;
    servo.attach(2);
    if (servo.attached() == true) {
      attivaServo = true;
      Serial.println("Servo riattivato dopo modalita' notte");
      stampaOrario();
    }
    var = false;
  }

  currentTime = millis();

  if (userMode == false && currentTime > waitTime + 60000 && scatto == true) {
    primoPassaggio = 0;
    servo.attach(2);
    if (servo.attached() == true) {
      attivaServo = true;
      Serial.println("Servo riattivato dopo click utente");
      stampaOrario();
    }

    scatto = false;
    countClick = 0; // l'utente puo' cliccare (= erogare) dopo che e' passato l'intervallo di disattivazione del servo
    waitTime = millis();
  }

  //  currentTime = millis();
  //
  //  if (userMode == false && currentTime > nightTime + attesa && scatto == true) { // valutare se inserire anche var == true
  //    primoPassaggio = 0;
  //    servo.attach(2);
  //    if (servo.attached() == true) {
  //      attivaServo = true;
  //      Serial.println("Servo riattivato dopo click utente in modalita' notte");
  //      stampaOrario();
  //    }
  //
  //    var = false;  // boh
  //    scatto = false;
  //    countClickN = 0;
  //    nightTime = millis();
  //
  //  }

}


void modNotte() {

  nightTime = millis();

  servo.detach();
  if (servo.attached() == false) {
    attivaServo = false;
  }

  pir = digitalRead(PIR_PIN);

  if (pir == 1) {
    passNotte++;
    erogazione = false;
    Serial.println("POST DI NOTTE");
    postDati(erogazione, userMode, mod);
    //getToView();
    stampaOrario();
  }

  if (var == false) {
    var = true;
  }

  delay(3000);
}


bool hourRange(int currentHour, int currentMinutes, int startHour, int startMinutes, int stopHour, int stopMinutes) {
  if (startHour < stopHour) {
    if (currentHour > startHour && currentHour < stopHour) {
      return true;
    }
    if (currentHour < startHour || currentHour > stopHour) {
      return false;
    }
    if (currentHour == startHour) { // se l'ora coincide vado a vedere i minuti
      if ((currentMinutes >= startMinutes && currentMinutes <= stopMinutes) || (currentMinutes >= startMinutes && currentMinutes > stopMinutes)) {
        return true;
      }
      else {
        return false;
      }
    }

    if (currentHour == stopHour) {
      if ((currentMinutes <= stopMinutes)) {
        return true;
      }
      else {
        return false;
      }
    }
  }

  if (startHour > stopHour) {
    if (currentHour > startHour || currentHour < stopHour) { // ad esempio startHour = 24, stopHour = 5, currentHour = 2
      return true;
    }
    if (currentHour < startHour && currentHour > stopHour) {
      return false;
    }
    if (currentHour == startHour) {
      if (currentMinutes >= startMinutes && currentMinutes <= stopMinutes) {
        return true;
      }
      else {
        return false;
      }
    }
  }

  if (startHour == stopHour) { // startHour == endHour
    if (currentHour > startHour || currentHour < stopHour) {
      return false;
    }
    if (currentHour == startHour) {
      if (currentMinutes >= startMinutes && currentMinutes < stopMinutes) { // currentMinutes <= stopMinutes --> mi fermo al minuto successivo
        return true;
      }
      else {
        return false;
      }
    }
  }
}


void lettura() {

  // stampo la situazione attuale del sistema, in termini di modalita' attiva, stato del servo, numero di passaggi effettuati

  if (currentTime > letturaDati + 5000) {
    timeClient.update();
    currentHour = timeClient.getHours();
    currentMinutes = timeClient.getMinutes();
    currentSeconds = timeClient.getSeconds();
    Serial.print(daysOfTheWeek[timeClient.getDay()]);
    Serial.print(", ");
    Serial.print(currentHour);
    Serial.print(":");
    Serial.print(currentMinutes);
    Serial.print(":");
    Serial.println(currentSeconds);

    Serial.print("Modalita' attiva: ");
    Serial.println(mod); // mod un intero/booleano -- 1 corrisponde a modGiorno, 0 corrisponde a modNotte

    Serial.print("Stato del servo: ");
    Serial.println(attivaServo);

    Serial.print("Stato del PIR: ");
    Serial.println(pir);

    // POST

    //postDati(erogazione, userMode, mod);

    // aggiorno

    letturaDati = millis();
  }
}


// funzione per manipolazione utente

void userInput(WiFiClient client) {

  // Aspetta finchè il client non manda qualche dato

  Serial.println("new client");
  while (!client.available()) { //tells you how many bytes are available to be read
    delay(1);
  }

  // Leggi la parte iniziale della richiesta (fino al primo ritorno a capo)

  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();

  // identifica il tipo di richiesta

  if (request.indexOf("/servoOpen") != -1) {
    if (mod == 1) { // giorno
      countClick++;
      erogazione = false; // clicco ma senza erogare
      if (countClick == 1) { // erogo solo la prima volta che l'utente clicca durante l'intervallo di disattivazione del servo
        erogazione = true; // clicco e erogo
        servo.attach(2);
        servo.write(180);
        delay(3000);
        servo.write(0);
        delay(3000);
        attivaServo = false;
        servo.detach();

        waitTime = millis();
      }

      Serial.println("POST CLICK GIORNO");
      postDati(erogazione, userMode, mod);
      //getToView();
      stampaOrario();

    }
    else { // notte
      countClickN++;
      erogazione = false;
      if (countClickN == 1) { // erogo solo la prima volta che l'utente clicca durante l'intervallo di disattivazione del servo
        erogazione = true;
        servo.attach(2);
        servo.write(180);
        delay(3000);
        servo.write(0);
        delay(3000);
        attivaServo = false;
        servo.detach();

        //nightTime = millis();
        timeClient.update();
        currentHour = timeClient.getHours();
        currentMinutes = timeClient.getMinutes();
        
        stopHour += (currentHour - startHour);
        stopMinutes += (currentMinutes - startMinutes);
      }

      Serial.println("POST CLICK NOTTE");
      postDati(erogazione, userMode, mod); 
      //getToView();
      stampaOrario();
    }
  }

  if (scatto == false) { // ragionare se va messo dentro l'if precedente
    scatto = true;
  }

  //  if (request.indexOf("/servoClose") != -1) {
  //    servo.detach();
  //  }

  // Ritorna la risposta del webserver
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html; charset=utf-8");
  client.println("Access-Control-Allow-Origin: *");
  client.println("Connection: close");
  client.println(""); //  serve assolutamente

  delay(1);
  Serial.println("Client disconesso");
  Serial.println("");

}

// POST dati

void postDati(bool e, bool u, bool m) { // i parametri sono erogazione, userMode e mod -- che corrispondono ai flag erogation, userMod e timeMod in Django

  String postData;
  StaticJsonDocument<200> doc; // cambiare vedendo effetivamente lo spazio che occupa

  doc["erogation"] = erogazione;
  doc["userMod"] = userMode;
  doc["timeMod"] = mod;

  serializeJson(doc, Serial); // stampo sul monitor seriale
  serializeJson(doc, postData); // salvo l'oggetto Json in una stringa

  HTTPClient http;
  http.begin("http://192.168.1.105:8000/dispenser/sensor/"); // indirizzo IP del server Django -- mettere lo / alla fine !
  //http.begin("http://192.168.43.37:8000/dispenser/sensor/"); // HUAWEI P30 lite
  //http.begin("http://192.168.1.35:8000/dispenser/sensor/");
  //http.begin("http://172.22.36.134:8000/dispenser/sensor/");
  //http.begin("http://172.17.196.174:8000/dispenser/sensor/");

  http.addHeader("Content-Type", "application/json");    //Specify content-type header

  int httpCode = http.POST(postData);   //Send the request
  Serial.println(postData);
  String payload = http.getString();    //Get the response payload

  Serial.println(httpCode);   //Print HTTP return code
  Serial.println(payload);    //Print request response payload

  http.end();  //Close connection

}

void stampaOrario() {

  timeClient.update();
  currentHour = timeClient.getHours();
  currentMinutes = timeClient.getMinutes();
  currentSeconds = timeClient.getSeconds();
  Serial.print(daysOfTheWeek[timeClient.getDay()]);
  Serial.print(", ");
  Serial.print(currentHour);
  Serial.print(":");
  Serial.print(currentMinutes);
  Serial.print(":");
  Serial.println(currentSeconds);

}
//
//void getToView(){
//  HTTPClient http;
//  http.begin("http://192.168.1.105:8000/dispenser/"); // indirizzo IP del server Django -- mettere lo / alla fine !
//  //http.begin("http://192.168.43.37:8000/dispenser/sensor/"); // HUAWEI P30 lite
//  //http.begin("http://192.168.1.35:8000/dispenser/sensor/");
//
//  //http.addHeader("Content-Type", "application/json");    //Specify content-type header
//
//  int httpCode = http.GET();   //Send the request
//  String payload = http.getString();    //Get the response payload
//
//  Serial.println(httpCode);   //Print HTTP return code
//  Serial.println(payload);    //Print request response payload
//
//  http.end();  //Close connection
//}
